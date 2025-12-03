#Const define by OptAdjust

#highlimit Setup
highlimit = {
'stmono_1_energy':      113,
'stmono_1_wavelength':  2.65,
'stmono_1_angle':       25,
'stmono_1_y1':          1000,
'stmono_1_theta':       497200,
'stmono_1_alpha1':      300000,
'stmono_1_phi1':        40000,
'stmono_1_x1':          90000,
'stmono_1_dtheta1':     1000000,
'stmono_1_z1':          45000,
'stmono_1_alpha2':      620000,
'stmono_1_phi2':        40000,
'stmono_1_x2':          90000,
'stmono_1_dtheta2':     1000000,
'stmono_1_z2':          45000,
'stmono_1_bend':        50000,
'slit_1_vertical':      10,
'slit_1_horizontal':    10,
'slit_1_height':        10,
'slit_1_width':         40,
'm100v_1_y':            20,
'm100v_1_z':            5,
'm100v_1_ty':           8,
'm100v_1_tz':           8,
'm100v_1_bend':         10000,
'm100v_2_y':            20,
'm100v_2_z':            10,
'm100v_2_ty':           8,
'm100v_2_tz':           8,
'm100v_2_bend':         10000,
'stmono_1_netplane':	511,
}
#lowlimit Setup
lowlimit = 	{
'stmono_1_energy':      4.6,
'stmono_1_wavelength':  0.17,
'stmono_1_angle':       3,
'stmono_1_y1':          -270000,
'stmono_1_theta':       -1000,
'stmono_1_alpha1':      -620000,
'stmono_1_phi1':        -40000,
'stmono_1_x1':          -90000,
'stmono_1_dtheta1':     -1000000,
'stmono_1_z1':          -95000,
'stmono_1_alpha2':      -300000,
'stmono_1_phi2':        -40000,
'stmono_1_x2':          -90000,
'stmono_1_dtheta2':     -1000000,
'stmono_1_z2':          -95000,
'stmono_1_bend':        -200000,
'slit_1_vertical':      -10,
'slit_1_horizontal':    -10,
'slit_1_height':        0,
'slit_1_width':         0,
'm100v_1_y':            -20,
'm100v_1_z':            -10,
'm100v_1_ty':           0,
'm100v_1_tz':           0,
'm100v_1_bend':         -100000,
'm100v_2_y':            -20,
'm100v_2_z':            -5,
'm100v_2_ty':           0,
'm100v_2_tz':           0,
'm100v_2_bend':         -100000,
'stmono_1_netplane':	111,
}

#SVOC Message
svoc_put = {
###################### - TAB_1 - ######################
 # Monochromator(standard type)						###
 	'stmono_1_netplane':    "put/bl_14b1_tc1_stmono_1_netplane/",			#35 111 / 311 / 511
	'stmono_1_energy':      "put/bl_14b1_tc1_stmono_1/",	        		#00 %fkev
	'stmono_1_wavelength':  "put/bl_14b1_tc1_stmono_1/",					#01 %fangstrome
	'stmono_1_angle':       "put/bl_14b1_tc1_stmono_1/",					#02 %fdegree
###################### - TAB_2 - ######################
 # Monochromator(pulse motor control)				###
	'stmono_1_y1':          "put/bl_14b1_tc1_stmono_1_y1/",					#03 %dpulse
	'stmono_1_theta':       "put/bl_14b1_tc1_stmono_1_theta/",				#04 %dpulse
	'stmono_1_alpha1':      "put/bl_14b1_tc1_stmono_1_alpha1/",				#05 %dpulse
	'stmono_1_phi1':        "put/bl_14b1_tc1_stmono_1_phi1/",				#06 %dpulse
	'stmono_1_x1':          "put/bl_14b1_tc1_stmono_1_x1/",					#07 %dpulse
	'stmono_1_dtheta1':     "put/bl_14b1_tc1_stmono_1_dtheta1/",			#08 %dpulse
	'stmono_1_z1':          "put/bl_14b1_tc1_stmono_1_z1/",					#09 %dpulse
	'stmono_1_alpha2':      "put/bl_14b1_tc1_stmono_1_alpha2/",				#10 %dpulse
	'stmono_1_phi2':        "put/bl_14b1_tc1_stmono_1_phi2/",				#11 %dpulse
	'stmono_1_x2':          "put/bl_14b1_tc1_stmono_1_x2/",					#12 %dpulse
	'stmono_1_dtheta2':     "put/bl_14b1_tc1_stmono_1_dtheta2/",			#13 %dpulse
	'stmono_1_z2':          "put/bl_14b1_tc1_stmono_1_z2/",					#14 %dpulse
	'stmono_1_bend':        "put/bl_14b1_tc1_stmono_1_bend/",				#15 %dpulse
###################### - TAB_3 - ######################
 # Viratula Axis type TC-Slit						###
	'slit_1_vertical':      "put/bl_14b1_tc1_slit_1_vertical/",				#16 %fmm
	'slit_1_horizontal':    "put/bl_14b1_tc1_slit_1_horizontal/",			#17 %fmm
	'slit_1_height':        "put/bl_14b1_tc1_slit_1_height/",				#18 %fmm
	'slit_1_width':         "put/bl_14b1_tc1_slit_1_width/",				#19 %fmm
###################### - TAB_4 - ######################
 # Viratula Axis type Mirror						###
	'm100v_1_y':            "put/bl_14b1_tc1_m100v_1_y/",					#20 %fmm
	'm100v_1_z':            "put/bl_14b1_tc1_m100v_1_z/",					#21 %fmm
	'm100v_1_ty':           "put/bl_14b1_tc1_m100v_1_ty/",					#22 %fmrad
	'm100v_1_tz':           "put/bl_14b1_tc1_m100v_1_tz/",					#23 %fmrad
	'm100v_1_bend':         "put/bl_14b1_tc1_m100v_1_bend/",				#24 %dpulse
	'm100v_2_y':            "put/bl_14b1_tc1_m100v_2_y/",					#25 %fmm
	'm100v_2_z':            "put/bl_14b1_tc1_m100v_2_z/",					#26 %fmm
	'm100v_2_ty':           "put/bl_14b1_tc1_m100v_2_ty/",					#27 %fmrad
	'm100v_2_tz':           "put/bl_14b1_tc1_m100v_2_tz/",					#28 %fmrad
	'm100v_2_bend':         "put/bl_14b1_tc1_m100v_2_bend/",				#29 %dpulse
###################### - TAB_? - ######################
 # speed of theta, alpha & phi 						###

 # MBS & DSS										###
#	'mbs':                  "put/bl_14b1_plc_mbs/",							#36 open / close
#	'dss':                  "put/bl_14b1_plc_dss_1/",						#37 open / close
#######################################################
}

svoc_get = {
###################### - TAB_1 - ######################
 # Monochromator(standard type)						###
 	'stmono_1_netplane':    "get/bl_14b1_tc1_stmono_1/netplane",			#35 111 / 311 / 511
	'stmono_1_energy':      "get/bl_14b1_tc1_stmono_1/energy",				#00 %fkev
	'stmono_1_wavelength':  "get/bl_14b1_tc1_stmono_1/wavelength",			#01 %fangstrome
	'stmono_1_angle':       "get/bl_14b1_tc1_stmono_1/angle",				#02 %fdegree
###################### - TAB_2 - ######################
 # Monochromator(pulse motor control)				###
	'stmono_1_y1':          "get/bl_14b1_tc1_stmono_1_y1/position",			#03 %dpulse
	'stmono_1_theta':       "get/bl_14b1_tc1_stmono_1_theta/position",		#04 %dpulse
	'stmono_1_alpha1':      "get/bl_14b1_tc1_stmono_1_alpha1/position",		#05 %dpulse
	'stmono_1_phi1':        "get/bl_14b1_tc1_stmono_1_phi1/position",		#06 %dpulse
	'stmono_1_x1':          "get/bl_14b1_tc1_stmono_1_x1/position",			#07 %dpulse
	'stmono_1_dtheta1':     "get/bl_14b1_tc1_stmono_1_dtheta1/position",	#08 %dpulse
	'stmono_1_z1':          "get/bl_14b1_tc1_stmono_1_z1/position",			#09 %dpulse
	'stmono_1_alpha2':      "get/bl_14b1_tc1_stmono_1_alpha2/position",		#10 %dpulse
	'stmono_1_phi2':        "get/bl_14b1_tc1_stmono_1_phi2/position",		#11 %dpulse
	'stmono_1_x2':          "get/bl_14b1_tc1_stmono_1_x2/position",			#12 %dpulse
	'stmono_1_dtheta2':     "get/bl_14b1_tc1_stmono_1_dtheta2/position",	#13 %dpulse
	'stmono_1_z2':          "get/bl_14b1_tc1_stmono_1_z2/position",			#14 %dpulse
	'stmono_1_bend':        "get/bl_14b1_tc1_stmono_1_bend/position",		#15 %dpulse
###################### - TAB_3 - ######################
 # Viratula Axis type TC-Slit						###
	'slit_1_vertical':      "get/bl_14b1_tc1_slit_1_vertical/position",		#16 %fmm
	'slit_1_horizontal':    "get/bl_14b1_tc1_slit_1_horizontal/position",	#17 %fmm
	'slit_1_height':        "get/bl_14b1_tc1_slit_1_height/aperture",		#18 %fmm
	'slit_1_width':         "get/bl_14b1_tc1_slit_1_width/aperture",		#19 %fmm
###################### - TAB_4 - ######################
 # Viratula Axis type Mirror						###
	'm100v_1_y':            "get/bl_14b1_tc1_m100v_1_y/position",			#20 %fmm
	'm100v_1_z':            "get/bl_14b1_tc1_m100v_1_z/position",			#21 %fmm
	'm100v_1_ty':           "get/bl_14b1_tc1_m100v_1_ty/angle",				#22 %fmrad
	'm100v_1_tz':           "get/bl_14b1_tc1_m100v_1_tz/angle",				#23 %fmrad
	'm100v_1_bend':         "get/bl_14b1_tc1_m100v_1_bend/position",		#24 %dpulse
	'm100v_2_y':            "get/bl_14b1_tc1_m100v_2_y/position",			#25 %fmm
	'm100v_2_z':            "get/bl_14b1_tc1_m100v_2_z/position",			#26 %fmm
	'm100v_2_ty':           "get/bl_14b1_tc1_m100v_2_ty/angle",				#27 %fmrad
	'm100v_2_tz':           "get/bl_14b1_tc1_m100v_2_tz/angle",				#28 %fmrad
	'm100v_2_bend':         "get/bl_14b1_tc1_m100v_2_bend/position",		#29 %dpulse
###################### - TAB_? - ######################
 # speed of theta, alpha & phi 						###


 # MBS & DSS										###
#	'mbs':                  "get/bl_14b1_plc_mbs/status",					#36 open / close
	#'dss':                  "get/bl_14b1_plc_dss_1/status",					#37 open / close
 # Ring Current										###
#	'ringcurrent':          "get/bl_dbci_ringcurrent/present",				#38 %fmA
#######################################################
}

svoc_query = {
###################### - TAB_1 - ######################
 # Monochromator(standard type)						###
 	'stmono_1_netplane':	"get/bl_14b1_tc1_stmono_1/query",
	'stmono_1_energy':      "get/bl_14b1_tc1_stmono_1/query",				#00
	'stmono_1_wavelength':      "get/bl_14b1_tc1_stmono_1/query",				#01
	'stmono_1_angle':      "get/bl_14b1_tc1_stmono_1/query",				#02
###################### - TAB_2 - ######################
 # Monochromator(pulse motor control)				###
	'stmono_1_y1':          "get/bl_14b1_tc1_stmono_1_y1/query",			#03
	'stmono_1_theta':       "get/bl_14b1_tc1_stmono_1_theta/query",			#04
	'stmono_1_alpha1':      "get/bl_14b1_tc1_stmono_1_alpha1/query",		#05
	'stmono_1_phi1':        "get/bl_14b1_tc1_stmono_1_phi1/query",			#06
	'stmono_1_x1':          "get/bl_14b1_tc1_stmono_1_x1/query",			#07
	'stmono_1_dtheta1':     "get/bl_14b1_tc1_stmono_1_dtheta1/query",		#08
	'stmono_1_z1':          "get/bl_14b1_tc1_stmono_1_z1/query",			#09
	'stmono_1_alpha2':      "get/bl_14b1_tc1_stmono_1_alpha2/query",		#10
	'stmono_1_phi2':        "get/bl_14b1_tc1_stmono_1_phi2/query",			#11
	'stmono_1_x2':          "get/bl_14b1_tc1_stmono_1_x2/query",			#12
	'stmono_1_dtheta2':     "get/bl_14b1_tc1_stmono_1_dtheta2/query",		#13
	'stmono_1_z2':          "get/bl_14b1_tc1_stmono_1_z2/query",			#14
	'stmono_1_bend':        "get/bl_14b1_tc1_stmono_1_bend/query",			#15
###################### - TAB_3 - ######################
 # Viratula Axis type TC-Slit						###
	'slit_1_vertical':      "get/bl_14b1_tc1_slit_1/query",					#16
	'slit_1_horizontal':    "get/bl_14b1_tc1_slit_1/query",					#17
	'slit_1_height':        "get/bl_14b1_tc1_slit_1/query",					#18
	'slit_1_width':         "get/bl_14b1_tc1_slit_1/query",					#19
###################### - TAB_4 - ######################
 # Viratula Axis type Mirror						###
	'm100v_1_y':            "get/bl_14b1_tc1_m100v_1/query",				#20
	'm100v_1_z':            "get/bl_14b1_tc1_m100v_1/query",				#21
	'm100v_1_ty':           "get/bl_14b1_tc1_m100v_1/query",				#22
	'm100v_1_tz':           "get/bl_14b1_tc1_m100v_1/query",				#23
	'm100v_1_bend':         "get/bl_14b1_tc1_m100v_1_bend/query",			#24
	'm100v_2_y':            "get/bl_14b1_tc1_m100v_2/query",				#25
	'm100v_2_z':            "get/bl_14b1_tc1_m100v_2/query",				#26
	'm100v_2_ty':           "get/bl_14b1_tc1_m100v_2/query",				#27
	'm100v_2_tz':          "get/bl_14b1_tc1_m100v_2/query",				#28
	'm100v_2_bend':         "get/bl_14b1_tc1_m100v_2_bend/query",			#29
#######################################################

}

#SVOC unit Setting
svoc_unit={
    'stmono_1_energy':      "kev",
    'stmono_1_wavelength':  "angstrome",
    'stmono_1_angle':       "degree",
    'stmono_1_y1':          "pulse",
    'stmono_1_theta':       "pulse",
    'stmono_1_alpha1':      "pulse",
    'stmono_1_phi1':        "pulse",        
    'stmono_1_x1':          "pulse",
    'stmono_1_dtheta1':     "pulse",
    'stmono_1_z1':          "pulse",
    'stmono_1_alpha2':      "pulse",
    'stmono_1_phi2':        "pulse",
    'stmono_1_x2':          "pulse",
    'stmono_1_dtheta2':     "pulse",
    'stmono_1_z2':          "pulse",
    'stmono_1_bend':        "pulse",
    'slit_1_vertical':      "mm",
    'slit_1_horizontal':    "mm",
    'slit_1_height':        "mm",
    'slit_1_width':         "mm",
    'm100v_1_y':            "mm",
    'm100v_1_z':            "mm",
    'm100v_1_ty':           "mrad",
    'm100v_1_tz':           "mrad",
    'm100v_1_bend':         "pulse",
    'm100v_2_y':            "mm",
    'm100v_2_z':            "mm",
    'm100v_2_ty':           "mrad",
    'm100v_2_tz':           "mrad",
    'm100v_2_bend':         "pulse",  
	'stmono_1_netplane':	"",  
}

#Mirror tilt config
#umit mirror_tilt(mrad):pulse
mirror_offset = -0.1

mirror_tcslit = {
1.0:0.4,
1.5:0.6,
2.0:0.8,
2.5:1.0,
3.0:1.2,
3.5:1.4,
4.0:1.6,
4.5:1.8,
5.0:2.0,
5.5:2.2,
6.0:2.4,
6.5:2.7,
7.0:3.0,
7.5:3.2,
8.0:3.4,
}
#umit mirror_tilt(mrad):pulse
m1_bend = {
1.0:-44500,
1.5:-42500,
2.0:-41000,
2.5:-39250,
3.0:-37500,
3.5:-35500,
4.0:-33500,
4.5:-30750,
5.0:-28000,
5.5:-26500,
6.0:-25000,
6.5:-23500,
7.0:-22000,
7.5:-20500,
8.0:-19000,
}
#umit mirror_tilt(mrad):pulse
m2_bend = {
1.0:-46000,
1.5:-46000,
2.0:-46000,
2.5:-46000,
3.0:-46000,
3.5:-46000,
4.0:-46000,
4.5:-46000,
5.0:-46000,
5.5:-46000,
6.0:-46000,
6.5:-46000,
7.0:-46000,
7.5:-46000,
8.0:-46000,
}

mirror_evacuation = {
'slit_1_height':1,
'm100v_1_bend': 0,
'm100v_2_bend': 0,
'm100v_1_ty':   0,
'm100v_2_ty':   0,
'm100v_1_z':    -10,
'm100v_2_z':    10,
}

mono_mode = {
'monoZZ':	9000,
'gamma':	0
}

white_mode = {
'monoZZ':	-135000,
'gamma':	-90000,
}