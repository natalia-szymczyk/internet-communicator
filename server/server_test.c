#include <stdio.h> 
#include <string.h>
#include <stdlib.h> 
#include <errno.h> 
#include <unistd.h>
#include <netdb.h>
#include <sys/types.h> 
#include <sys/socket.h> 
#include <sys/time.h>
#include <arpa/inet.h> 
#include <netinet/in.h> 
#include <sys/ioctl.h>
	
#define PORT 1100
          
int main(int argc , char *argv[]) 
{ 
	int opt = 1; 
  int master_socket;
  int new_socket;
  int sd;
  int max_sd;

	int client_socket[30];
  int max_clients = 30;  
	char user_list[30][50];
  int read_bytes_value;
  int i;

  char buffer[1025];
  char err_msg[250];
  fd_set readfds;
  FILE *users_fd;
    
	struct sockaddr_in address; 
  int addrlen;

  address.sin_family = AF_INET; 
	address.sin_addr.s_addr = INADDR_ANY; 
	address.sin_port = htons(PORT); 
  addrlen = sizeof(address);
  
  // active users
  memset(user_list, 0, sizeof user_list);
	
	//initialise all client_socket[] to 0 so not checked 
	for (i = 0; i < max_clients; i++) { 
		client_socket[i] = 0; 
	} 
		
	//create a master socket 
	if( (master_socket = socket(AF_INET , SOCK_STREAM , 0)) == 0) 
	{ 
		perror("socket failed"); 
		exit(EXIT_FAILURE); 
	} 
	
	//set master socket to allow multiple connections , 
	//this is just a good habit, it will work without this 
	if( setsockopt(master_socket, SOL_SOCKET, SO_REUSEADDR, (char *)&opt, sizeof(opt)) < 0) { 
		perror("setsockopt failed"); 
		exit(EXIT_FAILURE); 
	} 

// non blocking socket
  if (ioctl(master_socket, FIONBIO, (char *)&opt) < 0){
    perror("ioctl failed");
    close(master_socket);
    exit(EXIT_FAILURE);
  }

	//bind the socket to localhost port 8888 
	if (bind(master_socket, (struct sockaddr *)&address, sizeof(address))<0) 
	{ 
		perror("bind failed"); 
		exit(EXIT_FAILURE); 
	} 
		
	//try to specify maximum of 3 pending connections for the master socket 
	if (listen(master_socket, 3) < 0) 
	{ 
		perror("listen"); 
		exit(EXIT_FAILURE); 
	} 

	printf("Listener on port %d \n", PORT); 
		
	//accept the incoming connection 
	puts("Waiting for connections ..."); 

	while(1) 
	{ 
		//clear the socket set 
		FD_ZERO(&readfds); 

    // clear buffer
    memset(buffer, 0, sizeof buffer);
    memset(err_msg, 0, sizeof err_msg);

    strcpy(err_msg, "#ERR#");
	
		//add master socket to set 
		FD_SET(master_socket, &readfds); 
		max_sd = master_socket; 
			
		//add child sockets to set 
		for ( i = 0 ; i < max_clients ; i++) 
		{ 
			//socket descriptor 
			sd = client_socket[i]; 
				
			//if valid socket descriptor then add to read list 
			if(sd > 0) 
				FD_SET( sd , &readfds); 
				
			//highest file descriptor number, need it for the select function 
			if(sd > max_sd) 
				max_sd = sd; 
		} 
	
		//wait for an activity on one of the sockets , timeout is NULL , 
		//so wait indefinitely 	
		if ((select( max_sd + 1 , &readfds , NULL , NULL , NULL) < 0) && (errno!=EINTR)) 
		{ 
			printf("select error"); 
		} 
			
		//If something happened on the master socket , 
		//then its an incoming connection 
		if (FD_ISSET(master_socket, &readfds)) 
		{ 
			if ((new_socket = accept(master_socket, 
					(struct sockaddr *)&address, (socklen_t*)&addrlen))<0) 
			{ 
				perror("accept"); 
				exit(EXIT_FAILURE); 
			} 
			
			//inform user of socket number - used in send and receive commands 
			printf("New connection , socket fd is %d , ip is : %s , port : %d \n" , new_socket , 
              inet_ntoa(address.sin_addr) , ntohs (address.sin_port)); 
		
				
			puts("Welcome message sent successfully"); 
				
			//add new socket to array of sockets 
			for (i = 0; i < max_clients; i++) 
			{ 
				//if position is empty 
				if( client_socket[i] == 0 ) 
				{ 
          client_socket[i] = new_socket;
					printf("Adding to list of sockets as %d\n" , i); 
					break; 
				} 
			} 
		} 
			
		//else its some IO operation on some other socket 
		for (i = 0; i < max_clients; i++) 
		{ 
			sd = client_socket[i]; 
				
			if (FD_ISSET( sd , &readfds)) 
			{ 
				//Check if it was for closing , and also read the 
				//incoming message 
				if ((read_bytes_value = read( sd , buffer, 1024)) == 0) 
				{ 
					//Somebody disconnected , get his details and print 
					getpeername(sd , (struct sockaddr*)&address, (socklen_t*)&addrlen); 
					printf("Host disconnected , ip %s , port %d \n" , 
						inet_ntoa(address.sin_addr) , ntohs(address.sin_port)); 

          memset(user_list[i], 0, sizeof user_list[i]);

					close( sd ); 
					client_socket[i] = 0; 
				} 
					
				//Echo back the message that came in 
				else { 
          printf("%s\n",buffer);

          char *message = malloc(sizeof(buffer));
          strcpy(message,buffer);

          sleep(1);
          send(sd ,message,sizeof(message),0);
          memset(&buffer, 0, sizeof (buffer));


          }
				} 
			} 
		}  
		
	return 0; 
}