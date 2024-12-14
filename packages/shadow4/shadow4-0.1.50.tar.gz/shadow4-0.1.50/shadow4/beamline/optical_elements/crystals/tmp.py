import numpy
from shadow4.beamline.s4_beamline import S4Beamline

beamline = S4Beamline()

#
#
#
from shadow4.sources.source_geometrical.source_geometrical import SourceGeometrical
light_source = SourceGeometrical(name='SourceGeometrical', nrays=1000, seed=5676563)
light_source.set_spatial_type_point()
light_source.set_depth_distribution_off()
light_source.set_angular_distribution_flat(hdiv1=0.000000,hdiv2=0.000000,vdiv1=0.000000,vdiv2=0.000000)
light_source.set_energy_distribution_singleline(12914.000000, unit='eV')
light_source.set_polarization(polarization_degree=1.000000, phase_diff=0.000000, coherent_beam=1)
beam = light_source.get_beam()

BEAMS = [beam]

beamline.set_light_source(light_source)

# optical element number XX
from shadow4.beamline.optical_elements.crystals.s4_plane_crystal import S4PlaneCrystal
optical_element = S4PlaneCrystal(name='Plane Crystal',
    boundary_shape=None, material='Si',
    miller_index_h=8, miller_index_k=0, miller_index_l=0,
    f_bragg_a=False, asymmetry_angle=0.0,
    is_thick=1, thickness=0.001,
    f_central=1, f_phot_cent=0, phot_cent=12914.0,
    file_refl='Si(800)_12890_12940.dat',
    f_ext=0,
    material_constants_library_flag=0, # 0=xraylib,1=dabax,2=preprocessor v1,3=preprocessor v2
    method_efields_management=0, # 0=new in S4; 1=like in S3
    )
from syned.beamline.element_coordinates import ElementCoordinates
coordinates = ElementCoordinates(p=0, q=0.005657, angle_radial=0.7853355061, angle_azimuthal=-numpy.pi/2, angle_radial_out=0.7853355061)
movements = None
from shadow4.beamline.optical_elements.crystals.s4_plane_crystal import S4PlaneCrystalElement
beamline_element = S4PlaneCrystalElement(optical_element=optical_element,coordinates=coordinates, movements=movements, input_beam=beam)

beam, mirr = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)


BEAMS.append(beam)

# test plot
if 0:
   from srxraylib.plot.gol import plot_scatter
   plot_scatter(beam.get_photon_energy_eV(nolost=1), beam.get_column(23, nolost=1), title='(Intensity,Photon Energy)', plot_histograms=0)
   plot_scatter(1e6 * beam.get_column(1, nolost=1), 1e6 * beam.get_column(3, nolost=1), title='(X,Z) in microns')

#
# analysis
#

import numpy
print("##################################  beam intensities ################################")
for i in range(len(BEAMS)):
    print(f'tot: {BEAMS[i].get_intensity():.6g} s: {BEAMS[i].get_intensity(polarization=1):.6g} p: {BEAMS[i].get_intensity(polarization=2):.6g}')
print('\n')

r_s_ampl = -0.024724229926740865-0.9700768156818347j
r_p_ampl = 0.0009332843711563077+0.0011002464391183318j

r_s_ampl = 1
r_p_ampl = 1


r_s_mod = numpy.abs(r_s_ampl)
r_p_mod = numpy.abs(r_p_ampl)

r_s = r_s_mod ** 2 # 0.94166032
r_p = r_p_mod ** 2 # 2.08156194e-06

R_S = [r_s / 2**2] # ,r_s,r_s,r_s,    r_p, r_s, r_s, r_s]
R_P = [r_s / 2**2] # ,r_p,r_p,r_p,    r_s, r_p, r_p, r_p]

I_s = 1000 #* 1/2**2 * (r_s)**4
I_p = 1000 #* 1/2**2 * (r_p)**4

for i in range(len(R_S)):
    I_s *= R_S[i]
    I_p *= R_P[i]
    print("Analytical s,p (after %d crystals: ) " % (1+i), I_s, I_p )

print('\n')

print("##################################  Jones vectors ################################")
print("Jones vector at source: ",   BEAMS[0].get_jones()[0], "analytical_exact", [1,0],)
print("Jones vector after xtal1: ", BEAMS[1].get_jones()[0], "analytical_exact", [0.5 * r_s_ampl**1              , 0.5 * r_s_ampl    * r_p_ampl**0])
# print("Jones vector after xtal2: ", BEAMS[2].get_jones()[0], "analytical_exact", [0.5 * r_s_ampl**2              , 0.5 * r_s_ampl    * r_p_ampl**1])
# print("Jones vector after xtal3: ", BEAMS[3].get_jones()[0], "analytical_exact", [0.5 * r_s_ampl**3              , 0.5 * r_s_ampl    * r_p_ampl**2])
# print("Jones vector after xtal4: ", BEAMS[4].get_jones()[0], "analytical_exact", [0.5 * r_s_ampl**4              , 0.5 * r_s_ampl    * r_p_ampl**3])
# print("Jones vector after xtal5: ", BEAMS[5].get_jones()[0], "analytical_exact", [0.5 * r_s_ampl**4 * r_p_ampl   , 0.5 * r_s_ampl**2 * r_p_ampl**3])
# print("Jones vector after xtal6: ", BEAMS[6].get_jones()[0], "analytical_exact", [0.5 * r_s_ampl**5 * r_p_ampl   , 0.5 * r_s_ampl**2 * r_p_ampl**4])
# print("Jones vector after xtal7: ", BEAMS[7].get_jones()[0], "analytical_exact", [0.5 * r_s_ampl**6 * r_p_ampl   , 0.5 * r_s_ampl**2 * r_p_ampl**5])
# print("Jones vector after xtal8: ", BEAMS[8].get_jones()[0], "analytical_exact", [0.5 * r_s_ampl**7 * r_p_ampl   , 0.5 * r_s_ampl**2 * r_p_ampl**6])

print("##################################  Jones vectors modulus ################################")
print("Jones vector modulus at source: ",   numpy.abs(BEAMS[0].get_jones()[0]), "analytical", [1,0])
print("Jones vector modulus after xtal1: ", numpy.abs(BEAMS[1].get_jones()[0]), "analytical", [0.5 * r_s_mod**1              , 0.5 * r_s_mod    * r_p_mod**0])
# print("Jones vector modulus after xtal2: ", numpy.abs(BEAMS[2].get_jones()[0]), "analytical", [0.5 * r_s_mod**2              , 0.5 * r_s_mod    * r_p_mod**1])
# print("Jones vector modulus after xtal3: ", numpy.abs(BEAMS[3].get_jones()[0]), "analytical", [0.5 * r_s_mod**3              , 0.5 * r_s_mod    * r_p_mod**2])
# print("Jones vector modulus after xtal4: ", numpy.abs(BEAMS[4].get_jones()[0]), "analytical", [0.5 * r_s_mod**4              , 0.5 * r_s_mod    * r_p_mod**3])
# print("Jones vector modulus after xtal5: ", numpy.abs(BEAMS[5].get_jones()[0]), "analytical", [0.5 * r_s_mod**4 * r_p_mod    , 0.5 * r_s_mod**2 * r_p_mod**3])
# print("Jones vector modulus after xtal6: ", numpy.abs(BEAMS[6].get_jones()[0]), "analytical", [0.5 * r_s_mod**5 * r_p_mod    , 0.5 * r_s_mod**2 * r_p_mod**4])
# print("Jones vector modulus after xtal7: ", numpy.abs(BEAMS[7].get_jones()[0]), "analytical", [0.5 * r_s_mod**6 * r_p_mod    , 0.5 * r_s_mod**2 * r_p_mod**5])
# print("Jones vector modulus after xtal8: ", numpy.abs(BEAMS[8].get_jones()[0]), "analytical", [0.5 * r_s_mod**7 * r_p_mod    , 0.5 * r_s_mod**2 * r_p_mod**6])

print("Ray Intensity at source: ",   BEAMS[0].get_column(24)[0], BEAMS[0].get_column(25)[0], "analytical", 1,0,)
print("Ray Intensity after xtal1: ", BEAMS[1].get_column(24)[0], BEAMS[1].get_column(25)[0], "analytical", numpy.abs(0.5 * r_s_ampl**1           )**2   , numpy.abs(0.5 * r_s_ampl    * r_p_ampl**0)**2)
# print("Intensity after xtal2: ", BEAMS[2].get_column(24)[0], BEAMS[2].get_column(25)[0], "analytical", numpy.abs(0.5 * r_s_ampl**2           )**2   , numpy.abs(0.5 * r_s_ampl    * r_p_ampl**1)**2)
# print("Intensity after xtal3: ", BEAMS[3].get_column(24)[0], BEAMS[3].get_column(25)[0], "analytical", numpy.abs(0.5 * r_s_ampl**3           )**2   , numpy.abs(0.5 * r_s_ampl    * r_p_ampl**2)**2)
# print("Intensity after xtal4: ", BEAMS[4].get_column(24)[0], BEAMS[4].get_column(25)[0], "analytical", numpy.abs(0.5 * r_s_ampl**4           )**2   , numpy.abs(0.5 * r_s_ampl    * r_p_ampl**3)**2)
# print("Intensity after xtal5: ", BEAMS[5].get_column(24)[0], BEAMS[5].get_column(25)[0], "analytical", numpy.abs(0.5 * r_s_ampl**4 * r_p_ampl)**2   , numpy.abs(0.5 * r_s_ampl**2 * r_p_ampl**3)**2)
# print("Intensity after xtal6: ", BEAMS[6].get_column(24)[0], BEAMS[6].get_column(25)[0], "analytical", numpy.abs(0.5 * r_s_ampl**5 * r_p_ampl)**2   , numpy.abs(0.5 * r_s_ampl**2 * r_p_ampl**4)**2)
# print("Intensity after xtal7: ", BEAMS[7].get_column(24)[0], BEAMS[7].get_column(25)[0], "analytical", numpy.abs(0.5 * r_s_ampl**6 * r_p_ampl)**2   , numpy.abs(0.5 * r_s_ampl**2 * r_p_ampl**5)**2)
# print("Intensity after xtal8: ", BEAMS[8].get_column(24)[0], BEAMS[8].get_column(25)[0], "analytical", numpy.abs(0.5 * r_s_ampl**7 * r_p_ampl)**2   , numpy.abs(0.5 * r_s_ampl**2 * r_p_ampl**6)**2)

print("Es,p at source: ",   BEAMS[0].get_column(7)[0], BEAMS[0].get_column(8)[0], BEAMS[0].get_column(9)[0],",",
                            BEAMS[0].get_column(16)[0], BEAMS[0].get_column(17)[0], BEAMS[0].get_column(18)[0],)
print("Es,p after xtal1: ", BEAMS[1].get_column(7)[0],  BEAMS[1].get_column(8)[0],  BEAMS[1].get_column(9)[0],",",
                            BEAMS[1].get_column(16)[0], BEAMS[1].get_column(17)[0], BEAMS[1].get_column(18)[0],)

print("e_S, e_P at source:", BEAMS[0].get_efield_directions()[0][0],",", BEAMS[0].get_efield_directions()[1][0])
print("e_S, e_P at xtal1:",  BEAMS[1].get_efield_directions()[0][0],",", BEAMS[1].get_efield_directions()[1][0])


print("Orthogonal source: ", BEAMS[0].efields_orthogonal())
print("Orthogonal xtal1: ", BEAMS[1].efields_orthogonal())

print('\n')

"""
##################################  OLD  intensities ################################
##################################  beam intensities ################################
xtal 0 s: 1000 p: 0 tot: 1000 
xtal 1 s: 470.83 p: 0.00104078 tot: 470.831 
xtal 2 s: 443.362 p: 2.16645e-09 tot: 443.362 
xtal 3 s: 417.496 p: 4.5096e-15 tot: 417.496 
xtal 4 s: 393.14 p: 9.38701e-21 tot: 393.14 
xtal 5 s: 8.83958e-21 p: 0.000818345 tot: 0.000818345 
xtal 6 s: 8.32388e-21 p: 1.70344e-09 tot: 1.70344e-09 
xtal 7 s: 7.83827e-21 p: 3.54581e-15 tot: 3.54581e-15 
xtal 8 s: 7.38098e-21 p: 7.38082e-21 tot: 1.47618e-20 

>> r_S:  (-0.024724230126427403-0.9700768156827494j) 0.9416603158805275
>> r_P:  (0.0009332843726529948+0.0011002464316948817j) 2.081561930695614e-06
>>>>> e_S, perp vIn:  [-1.00000000e+00 -8.66010341e-17 -8.65901768e-17] 0.0
>>>>> e_P, perp vIn:  [ 1.22464680e-16 -7.07151108e-01 -7.07062451e-01] 0.0
    >>>>> e_S, perp vIn:  [-1.00000000e+00 -8.66010341e-17 -8.65901768e-17] 0.0
    >>>>> e_P, perp vIn:  [ 1.22464680e-16 -7.07151108e-01 -7.07062451e-01] 0.0
>>>>> axis, mod, perp vIn:  [ 9.99999992e-01  4.80732310e-32 -2.73691106e-48] 0.9999999921399523 1.9354096914833173e-48
>>>>> final ee_S, perp vOut:  [ 9.99999992e-01  4.80732310e-32 -2.73691106e-48] 3.5384124347854994e-48
>>>>> final ee_P, perp vOut:  [ 3.39950386e-32 -7.07151103e-01  7.07062446e-01] -5.551115123125783e-17
    >>>>> final ee_S, perp vOut:  [ 9.99999992e-01  4.80732310e-32 -2.73691106e-48] 3.5384124347854994e-48
    >>>>> final ee_P, perp vOut:  [ 3.39950386e-32 -7.07151103e-01  7.07062446e-01] -5.551115123125783e-17
>>>NEW s, c, angle:  0.00012537980434092574 -0.9999999921399523 179.99281626635627
>>>OLD s, c, angle:  0.0 -1.0 180.0
>>> J:  (0.024724230126427403+0.9700768156827494j) 0j 0j (-0.0009332843726529948-0.0011002464316948817j)
>>> |J|:  0.9703918362602436 0.0 0.0 0.001442761910606048
>>>> Orthogonal footprint:  1 -1.9351670301940945e-48 3.5384124347854994e-48 -5.551115123125783e-17

>>> reflected beam e_S, mod e_s [ 1.00000000e+00  4.80732314e-32 -2.73691108e-48] 1.0
>>> reflected beam e_P, mod e_P, e_S.e_P:  [ 3.39950389e-32 -7.07151108e-01  7.07062451e-01] 1.0 -1.9351670606151054e-48
>>> Intensity foot s, beam in s, foot p,  beam in p: 0.4433620613072347 0.4708301505329443 2.166449981640843e-12 1.0407809557574208e-06






##################################  NEW beam intensities ################################
##################################  beam intensities ################################
xtal 0 s: 1000 p: 0 tot: 1000 
xtal 1 s: 470.83 p: 0.00104078 tot: 470.831 
xtal 2 s: 443.362 p: 2.46644e-09 tot: 443.362 
xtal 3 s: 417.496 p: 1.43703e-11 tot: 417.496 
xtal 4 s: 393.14 p: 1.36295e-11 tot: 393.14 
xtal 5 s: 1.28344e-11 p: 0.000818345 tot: 0.000818345 
xtal 6 s: 4.83992e-11 p: 1.70343e-09 tot: 1.75183e-09 
xtal 7 s: 4.55228e-11 p: 3.54592e-15 tot: 4.55264e-11 
xtal 8 s: 4.2867e-11 p: 7.33803e-21 tot: 4.2867e-11

2:
>> r_S:  (-0.024724230126427403-0.9700768156827494j) 0.9416603158805275
>> r_P:  (0.0009332843726529948+0.0011002464316948817j) 2.081561930695614e-06
>>>>> e_S, perp vIn:  [-1.00000000e+00 -8.66010341e-17 -8.65901768e-17] 0.0
>>>>> e_P, perp vIn:  [ 1.22464680e-16 -7.07151108e-01 -7.07062451e-01] 0.0
>>>>> axis, mod, perp vIn:  [ 9.99999992e-01  4.80732310e-32 -2.73691106e-48] 0.9999999921399523 1.9354096914833173e-48
>>>>> final ee_S, perp vOut:  [ 9.99999992e-01  4.80732310e-32 -2.73691106e-48] 3.5384124347854994e-48
>>>>> final ee_P, perp vOut:  [ 3.39950386e-32 -7.07151103e-01  7.07062446e-01] -5.551115123125783e-17
>>>OLD s, c, angle:  0.0 -1.0 180.0
>>>NEW s, c, angle:  0.00012537980434092574 -0.9999999921399523 179.99281626635627
>>> J:  (0.024724229932093774+0.9700768080578993j) (3.0999191357314894e-06+0.0001216280413459714j) (1.1701501203767611e-07+1.37948682332706e-07j) (-0.000933284365317335-0.0011002464230468923j)
>>> |J|:  0.9703918286329175 0.00012166753856434099 1.808932060623265e-07 0.0014427618992658704
>>>> Orthogonal footprint:  1 -1.9351670301940945e-48 3.5384124347854994e-48 -5.551115123125783e-17

>>> reflected beam e_S, mod e_s [ 1.00000000e+00  4.80732314e-32 -2.73691108e-48] 1.0
>>> reflected beam e_P, mod e_P, e_S.e_P:  [ 3.39950389e-32 -7.07151108e-01  7.07062451e-01] 1.0 -1.9351670606151054e-48
>>> Intensity foot s, beam in s, foot p,  beam in p: 0.4433619186297892 0.47083014313144944 2.4664351424936415e-12 1.0407809721185967e-06

"""