def sdk_values (driver, driven, driverAttr, drivenAttr, dic_keyValues):

    #example use : sdk_values ('smile_ctl', 'bs_facial_lf', 'ty', 'smile', {0:0,1:1})
    for clave,valor in dic_keyValues.iteritems():
    
        cmds.setDrivenKeyframe (driven, at = drivenAttr, cd= driver + '.' + driverAttr, v= valor, dv =clave)
		



        

