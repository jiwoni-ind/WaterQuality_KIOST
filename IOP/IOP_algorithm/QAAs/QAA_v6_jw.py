'''
QAA v6 
http://www.ioccg.org/groups/Software_OCA/QAA_v6_2014209.pdf 
http://www.ioccg.org/groups/Software_OCA/QAA_v6.xlsm
There are inconsistencies between the pdf definition, and the spreadsheet
implementation. Notably, the spreadsheet uses Rrs throughout rather than
rrs. As well, absorption / scatter values are slightly off, and the a_ph
calculation uses wavelength-specific absorption rather than solely the 443
band.
Here, we use the pdf definition in all cases except the a_ph calculation -
using wavelength absorption prevents higher band a_ph estimates from 
flattening (bands > ~500nm). Where exact bands are requested (e.g. the 
reference band lambda0), this implementation uses the nearest available
band. This impacts the exact absorption/scattering values used, as well as
the calculation of xi with the band difference in the exponent. 
551 is also used to find the closest 555nm band, in order to avoid using 
the 555nm band of MODIS (which is a land-focused band). 
'''

# from scipy.interpolate import CubicSpline as Interpolate
# %%
from scipy.interpolate import interp1d as Interpolate
from pathlib import Path
import numpy as np

# %%
from utils import (
	set_outputs, optimize, get_required,	
	loadtxt, to_rrs, closest_wavelength, find_wavelength
)
from meta4IOP import (
	h0, h1, h2,
	g0_QAA_v6 as g0, 
	g1_QAA_v6 as g1,
)

# %%
@set_outputs(['a', 'aph', 'adg443', 'b', 'bbp']) # Define the output product keys
@optimize([]) # Define any optimizable parameters
def model(Rrs, wavelengths, *args, **kwargs):
	wavelengths = np.array(wavelengths)
	required = [443, 490, 555, 670]
	tol = kwargs.get('tol', 10) # allowable difference from the required wavelengths
	Rrs = get_required(Rrs, wavelengths, required, tol) # get values as a function: Rrs(443)
	rrs = get_required(to_rrs(Rrs(None)), wavelengths, required, tol)

	# wavelengths = np.delete(wavelengths, [9, 10, 11])
	# Rrs = np.delete(Rrs(None), [9, 10, 11], axis=2)
	# Rrs = get_required(Rrs, wavelengths, required, tol)

	get_band   = lambda k: closest_wavelength(k, wavelengths, tol=tol, validate=False)
	functional = lambda v: get_required(v, wavelengths, [], tol)

	absorb  = Interpolate( *loadtxt('D:/workspace/waterQuality/IOP/IOP_data/aw3.txt').T , fill_value = 'extrapolate')
	scatter = Interpolate( *loadtxt('D:/workspace/waterQuality/IOP/IOP_data/bbw3.txt').T, fill_value = 'extrapolate')

	# Invert rrs formula to find u
	u = functional( (-g0 + ((g0**2) + 4 * g1 * rrs(None)) ** 0.5) / (2 * g1) )

	ratio = rrs(443)/rrs(555)
	chi = np.log10((rrs(443)+rrs(490))/(rrs(555)+5*(rrs(670)/rrs(490))*rrs(670)))	

	QAA_v5 = Rrs(670) < 0.0015
	
	if QAA_v5.sum(): #Rrs670 < 0.0015
		lambda0     = get_band(555)
		a_lambda0   = absorb(lambda0)+10**(h0+(h1*chi)+(h2*chi**2))
		bbp_lambda0 = u(lambda0)*a_lambda0/(1-u(lambda0))-scatter(lambda0)
		Y           = 2*(1-1.2*np.exp(-0.9*ratio))
		bbp         = bbp_lambda0*(lambda0/wavelengths)**Y
		a           = (1-u(wavelengths))*(scatter(wavelengths)+bbp)/u(wavelengths)

		# a_full[QAA_v5] = a_lambda0[QAA_v5]
		# b_full[QAA_v5] = bbp_lambda0[QAA_v5]
		# l_full[QAA_v5] = lambda0

		# #555
		# a555 = absorb(555)+10**_tmp4
		# bbp555 = u(555)*a555/(1-u(555))-0.0009
		# Y = 2*(1-1.2*np.exp(-0.9*rrs(443)/rrs(555)))
		# bbp = bbp555*(555/wavelengths)**Y
		# a = (1-u(wavelengths))*(scatter(wavelengths)+bbp)/u(wavelengths)

	elif (~QAA_v5).sum(): #!(Rrs670 < 0.0015)
		lambda0     = get_band(670)
		a_lambda0   = absorb(670)+0.39*(rrs(670)/(rrs(443)+rrs(490)))**1.14
		bbp_lambda0 = u(lambda0)*a_lambda0/(1-u(lambda0))-scatter(lambda0)
		Y           = 2*(1-1.2*np.exp(-0.9*ratio))
		bbp         = bbp_lambda0*(lambda0/wavelengths)**Y
		a           = (1-u(wavelengths))*(scatter(wavelengths)+bbp)/u(wavelengths)


		# a_full[~QAA_v5] = a_lambda0[~QAA_v5]
		# b_full[~QAA_v5] = bbp_lambda0[~QAA_v5]
		# l_full[~QAA_v5] = lambda0

		# #670
		# aw670 = 0.439
		# bbw670 = 0.00034
		# a670 = aw670+0.39*_tmp1**1.14
		# bbp670 = u(670)*a670/(1-u(670))-bbw670
		# Y = 2*(1-1.2*np.exp(-0.9*(rrs(443)/rrs(555))))
		# bbp = bbp670*(670/wavelengths)**Y
		# a = (1-u(wavelengths))*(scatter(wavelengths)+bbp)/u(wavelengths)
	bbp = get_required(bbp, wavelengths, [], tol)
	a   = get_required(a, wavelengths, [], tol)

	S = 0.015+0.002/(0.6+ratio)	
	xi = np.exp(S*(443-412))
	zeta = 0.74+0.2/(0.8+(ratio))
	
	#!!!!
	adg443 = (a(412)-zeta*a(443)-absorb(412)+zeta*absorb(443))/((xi-zeta))
	aph    = a(wavelengths) -absorb(wavelengths)-adg443*np.exp(S*(443-wavelengths))

	a = a(wavelengths)
	adg443 = adg443
	aph = aph
	bb = scatter(wavelengths) + bbp(wavelengths)
	bbp = bbp(wavelengths)
	
	# Return all backscattering and absorption parameters
	return {
		'a'  : a,
		'aph': aph,
		'adg443': adg443, 
		'bb'  : bb,
		'bbp': bbp,
	}