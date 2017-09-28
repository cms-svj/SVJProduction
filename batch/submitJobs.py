from jobSubmitterSVJ import jobSubmitterSVJ

def submitJobs():  
    mySubmitter = jobSubmitterSVJ()
    mySubmitter.run()
    
if __name__=="__main__":
    submitJobs()
