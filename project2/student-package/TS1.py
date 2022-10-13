# Step1: Open socket connection on ts1 side
# Step2: Bind to the (ip,port) pair and listen for rs connections.
# Step3: In a loop, accept connection from rs.
# Receive query from rs and decode it.
# open the "PROJ2-DNSTS1.txt" file (can read this file and load into a dictionary).
# check if query is present, if present send response.
# else do nothing.close socket connection with rs.
# Step4: close the socket connection and exit.