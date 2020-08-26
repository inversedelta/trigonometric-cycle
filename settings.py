conf = {
		# GLOBAL
		'speed' : .6,
		'drawcartlines' : True,
		'bgklr' 		: [230, 230, 230],
		'planelineskl'  : [185, 185, 185],


		# CIRCLE
		'circlepos'  : [500, 300],
		'radius' : 128,
		'bd' : 1,
		'bdklr' 		: [175, 175, 175],
		'circle_klr' 	: [240, 240, 240],
		'drawbd' : False,

		
		# RADIUS
		'radwidth' : 1,
		'drawradline' 	: False,
		'drawradpoints' : False,
		'radiusklr' : [20, 20, 20],


		# SIN / COS
		'dklr' : .7,			# factor of color transition
		'dwcosin' : .8, 		# change of width of the cosine or sine line
		'widthcosin' : 8,
		'drawsin' 		: True,
		'drawcos' 		: True,
		'drawtrifill' 	: True,
		'triangklr'	: [210, 210, 210],
		'cosklr' 	: [46, 40, 255],
		'sinklr' 	: [255, 40, 46],



		# TANGENT / COTAN
		'tgwidth' : 2,
		'radtgwidth' : 1,
		'drawtg' 		: True,
		'drawcotg' 		: True,
		'drawtgline' 	: False, # needs drawtg
		'drawcotgline' 	: False,
		'drawtgenddot'	: False,
		'tgklr' : (20, 20, 20),
		


		# SECANT / COSEC
		'widthcossec' : 1,
		'widthcnectcossec' : 1,	
		'drawsec' 		: True,
		'drawcosec' 	: True,
		'connectcossec' : False,
		'cossecfill'	: True,
		'cossecfillklr'		: [215, 215, 190],
		'connectcossecklr'	: [80, 100, 80],
		'cossecklr' 		: [0, 100, 0],
}