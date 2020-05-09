from jobSubmitterSUEP import jobSubmitterSUEP

def submitJobs():  
    mySubmitter = jobSubmitterSUEP()
    mySubmitter.run()
    
if __name__=="__main__":
    submitJobs()
