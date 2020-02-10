#This script copies the files from git folder across social media sites to secure thumbdrive
#Copying the file to secured thumbdrive -->/media/jirong/Secure Key/stb_social_media/tripadvisor/finalised_output
library(dplyr)
library(R.utils)
library(yaml)

config = read_yaml("./config_file.yml")

#config parameter for personal directory
thumb_dir = paste0(config$General$thumb_dir, "/tripadvisor/finalised_output")

########################################Tripadvisor#################################################
copy_trip = function() {

#Read to_be_processed.csv
trip_processed = read.csv("./tripadvisor/to_be_processed.csv", stringsAsFactors = F)
trip_copied = read.csv("./tripadvisor/is_copied_files.csv", stringsAsFactors = F)

#Initialize log files
log = data.frame(message = c("init"), stringsAsFactors = F)
filename = paste0("./tripadvisor/processed_copied_log_files/", gsub(":", "_",Sys.time()), ".csv")
write.csv(log, filename, row.names = F)  
 
#Check if trip_processed has unique datetime
if (length(unique(trip_processed$DATE_TIME)) == nrow(trip_processed)){
  
  #Determine which folders are not copied yet (check csv in git folder)
  trip_processed_rdy = trip_processed %>%
                        dplyr::filter(IS_READY == 1)
  
  trip_processed_rdy = trip_processed_rdy[which(!(trip_processed_rdy$DATE_TIME %in% trip_copied$DATE_TIME)), ]
  
  #If processed dataset and the processed csv is unique, proceed to add. If not flag out as error 
  data_combined = rbind(trip_processed_rdy, trip_copied)
  
  if((nrow(data_combined) == length(unique(data_combined$DATE_TIME))) & nrow(trip_processed_rdy) != 0){

    #try-catch block
    #Copy operations to thumbdrive
    for(i in 1:nrow(trip_processed_rdy)){
      
      #print(i)
      
      tryCatch({
        folder = paste0(thumb_dir, "/", trip_processed_rdy$DATE_TIME[i])

        if(dir.exists(folder)){

          folder_exists = paste0(folder, " exists. Can't copy content")
          message(folder_exists)

          write.table(data.frame(message = c(folder_exists), stringsAsFactors = F),
                      file=filename,
                      append = T,
                      sep=',',
                      row.names=F,
                      col.names=F)

          next   #skip current folder index

        }else{
          dir.create(folder)
        }

        copyDirectory(from = paste0("./tripadvisor/finalised_output/", trip_processed_rdy$DATE_TIME[i]),
                      to = folder,
                      recursive = T)

        message(paste0("Add ",  trip_processed_rdy$DATE_TIME[i], " folder"))

        write.table(trip_processed_rdy[i, ],
                    file="./tripadvisor/is_copied_files.csv",
                    append = T,
                    sep=',',
                    row.names=F,
                    col.names=F)

      }, error = function(e){
        msg_cant_copy = paste0("Error in copying tripadvisor folder: ", trip_processed_rdy$DATE_TIME[i])
        write.table(data.frame(message = c(msg_cant_copy), stringsAsFactors = F),
                    file=filename,
                    append = T,
                    sep=',',
                    row.names=F,
                    col.names=F)
      })
            
    }
    
  }else{
    
    if( nrow(trip_processed_rdy) == 0 ){
      msg = "no data files to add"  
    }else{
      msg = "to be combined dataset in is_copied_files.csv doesnt have unique date_time"
    }    
    
    write.table(data.frame(message = c(msg), stringsAsFactors = F),
                file=filename,
                append = T,
                sep=',',
                row.names=F,
                col.names=F)
    message(msg)
  }  
  
}else{
  
  msg = "to_be_processed.csv doesnt have unique date_time"    
  
  write.table(data.frame(message = c(msg), stringsAsFactors = F),
              file=filename,
              append = T,
              sep=',',
              row.names=F,
              col.names=F)
  message(msg)
}
 
message("copy_trip function ran")

}
