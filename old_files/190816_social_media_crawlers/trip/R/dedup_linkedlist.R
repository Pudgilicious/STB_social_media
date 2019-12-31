#Note: De-deuplicate linked list using what I crawled and NUS crawled
#Copied res_link_list (from NUS) and trip_res_link.txt (my version) into csv res_link_b4_dedup

#Read in data
res_link_b4_dedup <- read.table("./output_archived_190817/res_link_b4_dedup.csv", quote="\"", comment.char="", stringsAsFactors = F)
  
#dedup
res_link_dedup = data.frame(links = res_link_b4_dedup[!duplicated(res_link_b4_dedup$V1),])

#Write out as text file
write.table(res_link_dedup, "./output_archived_190817/res_link_dedup.txt", row.names = F)
write.csv(res_link_dedup, "./output_archived_190817/res_link_dedup.csv", row.names = F)

#Manually copy to txt file (res_link_dedup) to remove inverted commas