anemia=[['tired',30,0],['head_ache',10,0],['pale',80,0],['heart_rapid',30,0],['breathe_rapid',80,0]]

appendicitis=[['abdominal_pain',15,0],['appetite_loss',20,0],['nausea',80,0],['constipated',80,0],['diarrhea',20,0]]

bladder_infection=[['abdominal_pain',25,0],['discomfort',80,0],['urinate_pain',25,0]]

brain_tumor=[['head_ache',15,0],['change_speech',80,0],['change_vision',80,0],['change_hearing',80,0],['convulsions',15,0],['loss_balance',80,0],['concentration_lost',80,0]]

cancer=[['fatigue',10,0],['weakness',10,0],['weight_loss',10,0],['no_urinate',80,0],['skin_change',80,0],['cough',10,0],['bleeding',10,0],['lumps',80,0]]

dengue=[['fever',15,0],['head_ache',15,0],['pain_eyes',80,0],['bleeding',15,0],['lower_back_pain',15,0],['joint_pain',20,0]]

depression=[['helplessness',80,0],['worthlessness',80,0],['guilt',80,0],['appetite_loss',20,0]]

diabities=[['vomiting',15,0],['appetite_increase',60,0],['urinate_increase',80,0],['weigth_loss',15,0],['weigth_gain',60,0],['nausea',15,0]]

flu=[['fever',15,0],['cough',15,0],['chills',15,0],['head_ache',15,0],['sore_throat',15,0],['diarrhea',15,0]]

hiv=[['fever',15,0],['muscle_ache',60,0],['urinate_increase',80,0],['sore_throat',15,0],['chills',15,0]]

hyperthermia = [['muscle_cramp',30,0],['fatigue',15,0],['dizziness',80,0],['nausea',15,0],['vomiting',15,0],['weakness',15,0],['mental_confusion',80,0]]

kidney_stone = [['low_back_pain',15,0],['sweating',30,0],['nausea',15,0],['vomiting',15,0],['urine_blood',80,0],['urinate_pain',15,0],['testicular pain',80,0]]

leukemia=[['fever',15,0],['night_sweat',50,0],['swollen_lymph_nodes',30,0],['weight_loss',15,0],['joint_pain',20,0],['nose_bleeding',80,0],['skin_patches',80,0]]

sinus_infection=[['facial_swelling',80,0],['nasal_congesstion',80,0],['ear_ache',80,0],['jaw_pain',80,0],['sore_throat',15,0],['bad_breath',80,0]]

stomach_ulcer=[['abdominal_pain',20,0],['indigestion',80,0],['appetite_loss',25,0],['weight_loss',25,0]]

strep_throat=[['sore_throat',20,0],['tonsils',80,0],['swallow_pain',80,0],['vomiting',20,0],['skin_rash',80,0]]

asthma = [['shortness_breath',50,0],['chest_tightness',80,0],['wheezing_sound',80,0],['trouble_sleep',30,0]]

malaria = [['chills',20,0],['fever',20,0],['sweating',30,0],['vomiting',20,0],['tired',30,0],['weakness',10,0],['skin_pale',80,0],['heart_rapid',30,0],['breath_short',50,0],['convulsions',15,0]]

cholera=[['heart_rapid',30,0],['less_skin_elasticity',80,0],['muscle_cramps',30,0],['thirst',30,0],['low_blood_pressure',80,0]]

jaundice=[['skin_yellow',80,0],['dark_urine',80,0],['pale_stools',80,0],['itchiness',60,0],['abdominal_pain',15,0]]


diseases=[['anemia',anemia],['appendicitis',appendicitis],['bladder_infection',bladder_infection],['brain_tumor',brain_tumor],['cancer',cancer],['dengue',dengue],['depression',depression],['diabities',diabities],['flu',flu],['hiv',hiv],['hyperthermia',hyperthermia],['kidney_stone',kidney_stone],['leukemia',leukemia],['sinus_infection',sinus_infection],['stomach_ulcer',stomach_ulcer],['strep_throat',strep_throat],['asthma',asthma],['malaria',malaria],['cholera',cholera],['jaundice',jaundice]]
symtoms_all=[]
fixd = []
twos=[]
threes=[]
variable=[]
for x in diseases:
		v = x[1]
		for j in v:
			symtoms_all.append(j[0])

	# for element in v:
	# 	if(element not in v):
	# 		symtoms_all. 
#print(symtoms_all)
for l in symtoms_all:
	if l.count('_')==1 :
		twos.append(l)
	elif l.count('_')==2 :
		threes.append(l)
	if l.count('_')==0 :
			fixd.append(l)
	else:
		variable = l.split('_')
		fixd.extend(variable)
		

#print(twos)
#print(threes)
#print(fixd)
