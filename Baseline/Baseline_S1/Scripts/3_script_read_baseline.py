#!/bin/bash

import sys
import os
import openpyxl
import pandas as pd
import math
import numpy as np
import statistics

def list_subdirs(in_path):
    matches = []
    for root, dirnames, filenames in os.walk(in_path):
        row=[]
        if(os.path.join(root).count("/")==3):
            matches.append(os.path.join(root)) 
    return matches
    

#COMPUTATION OF THE EXPECTED OUTCOME
def compute_oracle(spo2, hr, temp, sys_bp, dias_bp, glu):

    output=""

    all_sensors=[]
    all_sensors.append(spo2)
    all_sensors.append(hr)
    all_sensors.append(temp)
    all_sensors.append(sys_bp)
    all_sensors.append(dias_bp)
    all_sensors.append(glu)

    amount_high=0
    amount_med=0
    amount_low=0
    amount_deactivated=0

    for item in all_sensors:
         if(item=="low risk"):
             amount_low=amount_low+1
         elif(item=="moderate risk"):
             amount_med=amount_med+1
         elif(item=="high risk"):
             amount_high=amount_high+1
         elif(item=="deactivated"):
             amount_deactivated=amount_deactivated+1

    total= amount_high+amount_med+amount_low

    #if (total!=6):
    #	return "Error"

    if (amount_low==total):
        return "VERY LOW RISK"

    elif (amount_med==1 and amount_high==0):
        return "LOW RISK"

    elif (amount_med>=2 and amount_high==0):
        return "MODERATE RISK"

    elif (amount_high==1):
        return "CRITICAL RISK"

    elif (amount_high>1):
        return "VERY CRITICAL RISK"

    else: 
        return "ERROR!"
        
        

def read_output_prob_t2(j,resulting_file_name,patients_folder):

    content=[]
    
    # Create a new Excel workbook
    workbook = openpyxl.Workbook()
    # Select the default sheet (usually named 'Sheet')
    sheet = workbook.active

    result=[]
    sum_diff=[0,0,0,0,0]
    
    content.append(["Id","Patient","Oxi","Ecg","Term","Abps","Abpd","Glc","BSN Outcome","Expected Outcome","Difference","Oxi-Risk","Ecg-Risk","Term-Risk","Abps-Risk","Abpd-Risk","Glc-Risk","Oxi-Sens","Ecg-Sens","Term-Sens","Abps-Sens","Abpd-Sens","Glc-Sens","Timestamp"])

    term_sensor="0"
    ecg_sensor="0"
    oxi_sensor="0"
    abps_sensor="0"
    abpd_sensor="0"
    glc_sensor="0"
    sensor_values=False
    id=0
    
 
    id_outcome=0
    id_oracle=0
    id_difference=0
	    
	    
    directories = list_subdirs(patients_folder)

    for path in directories:
            
    	    BSN_output_folder=path+"/output_"+str(j)
    	    	    
	    ini_state_term=0
	    ini_state_ecg=0
	    ini_state_oxi=0
	    ini_state_abps=0
	    ini_state_abpd=0
	    ini_state_glc=0
  
            txt_files=[]
            for file in os.listdir(path):
               if file.endswith(".txt"):
                   txt_files.append(os.path.join(path, file))
                   
            for txt in txt_files:
               if (os.path.basename(txt)=="HR_mc.txt"):
	    	    ini_state_ecg=1
               elif(os.path.basename(txt)=="SaO2_mc.txt"):
		    ini_state_oxi=1 
               elif(os.path.basename(txt)=="Temp_mc.txt"):
		    ini_state_term=1
               elif(os.path.basename(txt)=="NISysABP_mc.txt"):
		    ini_state_abps=1 
               elif(os.path.basename(txt)=="NIDiasABP_mc.txt"):
		    ini_state_abpd=1
               elif(os.path.basename(txt)=="Glc_mc.txt"):
		    ini_state_glc=1
            
			   

	    if(os.path.isfile(BSN_output_folder+'/g4t1_-1-stdout.log')):
	       with open(BSN_output_folder+'/g4t1_-1-stdout.log') as f:
	            
	    	    id_outcome=0
		    id_oracle=0
		    id_difference=0
		    		   
		    x = f.readline() 
		    for line in f:
		                           		        
		        if(line.startswith("++++++++++++++++++++")):
		    	            line = next(f, None)
		    	            term_sensor=line[5:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            ecg_sensor=line[5:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            oxi_sensor=line[5:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            abps_sensor=line[6:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            abpd_sensor=line[6:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            glc_sensor=line[5:len(line)-1]
		    	            
		    	            next(f, None) #skip ++++++++++++++++++++
		    	            
		    	            line = next(f, None)
		    	            term=line[6:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            ecg=line[5:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            oxi=line[5:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            abps=line[6:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            abpd=line[6:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            glc=line[5:len(line)-1]
		    	            
		    	            line = next(f, None)#skip unecessary lines
		    	            line = next(f, None)#skip unecessary lines
		    	            line = next(f, None)#skip unecessary lines
		    	            line = next(f, None)#skip unecessary lines
		    	            
		    	            line = next(f, None)
		    	            term_risk=line[14:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            ecg_risk=line[12:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            oxi_risk=line[13:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            abps_risk=line[13:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            abpd_risk=line[13:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            glc_risk=line[12:len(line)-1]
		    	            
		    	            line = next(f, None)
		    	            resultado=line[16:(len(line)-1)]
		    	            
		    	            line = next(f, None)
		    	            time=line[25:(len(line)-1)]
		    	            
		    	            if((term!="unknown" or ini_state_term==0) and (ecg!="unknown" or ini_state_ecg==0) and (oxi!="unknown" or ini_state_oxi==0) and (abps!="unknown" or ini_state_abps==0) and (abpd!="unknown" or ini_state_abpd==0) and (glc!="unknown" or ini_state_glc==0)):
		    	            
					if(ini_state_term==0):
					   term="deactivated"
				        if(ini_state_ecg==0):
					   ecg="deactivated"
				        if(ini_state_oxi==0):
				 	   oxi="deactivated"
				        if(ini_state_abps==0):
					   abps="deactivated"
				        if(ini_state_abpd==0):
					   abpd="deactivated"
				        if(ini_state_glc==0):
					   glc="deactivated"
				     
				        oracle=compute_oracle(oxi,ecg,term,abps, abpd, glc)
				        if (resultado=="VERY LOW RISK"):
				           id_outcome=0
				        elif (resultado=="LOW RISK"):
				           id_outcome=1
				        elif (resultado=="MODERATE RISK"):
				           id_outcome=2
				        elif (resultado=="CRITICAL RISK"):
				           id_outcome=3
				        elif (resultado=="VERY CRITICAL RISK"):
				           id_outcome=4
				        else:
				           id_outcome=9999999999999

				        if (oracle=="VERY LOW RISK"):
				           id_oracle=0
				        elif (oracle=="LOW RISK"):
				           id_oracle=1
				        elif (oracle=="MODERATE RISK"):
				           id_oracle=2
				        elif (oracle=="CRITICAL RISK"):
				           id_oracle=3
				        elif (oracle=="VERY CRITICAL RISK"):
				           id_oracle=4
				        else:
				           id_oracle=9999999999999
				        id_difference=abs(id_outcome-id_oracle)
				        content.append([str(id),os.path.basename(path),oxi,ecg,term,abps,abpd,glc,resultado,oracle,str(id_difference), oxi_risk,ecg_risk,term_risk,abps_risk,abpd_risk, glc_risk,oxi_sensor, ecg_sensor,term_sensor, abps_sensor, abpd_sensor,glc_sensor,time])
				        sum_diff[id_difference]=sum_diff[id_difference]+1
				        id=id+1
		                                      
    
    tot_diff=sum_diff[0]+sum_diff[1]+sum_diff[2]+sum_diff[3]+sum_diff[4]
    tot_diff_perc=[]

    tot_diff_perc.append(sum_diff[0]*100/float(tot_diff))
    tot_diff_perc.append(sum_diff[1]*100/float(tot_diff))
    tot_diff_perc.append(sum_diff[2]*100/float(tot_diff))
    tot_diff_perc.append(sum_diff[3]*100/float(tot_diff))
    tot_diff_perc.append(sum_diff[4]*100/float(tot_diff))
	  
    content.append([])
    content.append(["","Absolute Amount","Percentage Amount"])
    content.append(["Difference 0", sum_diff[0],str(tot_diff_perc[0])+""])
    content.append(["Difference 1", sum_diff[1],str(tot_diff_perc[1])+"","","Passing TC Rate:"])
    content.append(["Difference 2", sum_diff[2],str(tot_diff_perc[2])+"","",str(float("{:.2f}".format(tot_diff_perc[0]+tot_diff_perc[1])))+""])
    content.append(["Difference 3", sum_diff[3],str(tot_diff_perc[3])+""])
    content.append(["Difference 4", sum_diff[4],str(tot_diff_perc[4])+""])
    content.append([])
    content.append([])
    content.append(["Sum",tot_diff,str(tot_diff_perc[0]+tot_diff_perc[1]+tot_diff_perc[2]+tot_diff_perc[3]+tot_diff_perc[4])+""])
  
    
    for row in content:
	sheet.append(row)
	    
    # Save the workbook to a file
    workbook.save("../Output_files/output"+str(j)+"_"+resulting_file_name)
    print(str(float("{:.2f}".format(tot_diff_perc[0]+tot_diff_perc[1]))))
    #print(tot_diff)
    return (tot_diff_perc[0]+tot_diff_perc[1])
 


def main(argv):
     
    if(len(sys.argv)==3):
       patients_folder= sys.argv[1]    
    elif(len(sys.argv)==1):
       patients_folder="../DTMCs"
    else:
       print("Error!")
       exit(0)
     
    number_of_executions=5
    passing_tc_rate=[]
     
    for j in range(0,number_of_executions):
       passing_tc_rate.append(read_output_prob_t2(j,'output_sensor_readings.xlsx',patients_folder))
  

        
if __name__ == "__main__":
    main(sys.argv)
