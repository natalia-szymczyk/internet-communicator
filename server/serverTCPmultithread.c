#include<stdio.h>
#include<stdlib.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<string.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <unistd.h> 
#include<pthread.h>

// gcc -g -Wall -pthread yourcode.c -lpthread -o yourprogram

#define HOST "172.27.82.106"
#define PORT 8858
#define MAX_CLIENTS 50
#define MSG_SIZE 2048

char client_message[MSG_SIZE];
unsigned int client_number = 0;
static int uid = 10;

pthread_mutex_t clients_mutex = PTHREAD_MUTEX_INITIALIZER;

typedef struct Client{
	struct sockaddr_storage address;
	int sockfd;
	int uid;
	char login[32];
} Client;

Client *clients[MAX_CLIENTS];


// send message to user with defined login
void send_message(char *s, char* login){
	pthread_mutex_lock(&clients_mutex);

	for(int i = 0; i < MAX_CLIENTS; ++i){
		if(clients[i]){
			if(strcmp(clients[i]->login, login) == 0 ){
        if(send(clients[i]->sockfd, s, strlen(s), 0) < 0){
          perror("ERROR: Sending failed");
          break;
        }
      }			
		}
	}

	pthread_mutex_unlock(&clients_mutex);
}

// add client to the list of clients
void add_client(Client *client){
	pthread_mutex_lock(&clients_mutex);

	for(int i = 0; i < MAX_CLIENTS; ++i){
		if(!clients[i]){
			clients[i] = client;
			break;
		}
	}

	pthread_mutex_unlock(&clients_mutex);
}

// remove client from the list of clients
void remove_client(int uid){
	pthread_mutex_lock(&clients_mutex);

	for(int i = 0; i < MAX_CLIENTS; ++i){
		if(clients[i]){
			if(clients[i]->uid == uid){
				clients[i] = NULL;
				break;
			}
		}
	}

	pthread_mutex_unlock(&clients_mutex);
}

// print all active users
void print_users(){
	pthread_mutex_lock(&clients_mutex);

  printf("\n\n---------------------------------------------------");
  printf("\nACTIVE USERS:\n");

	for(int i = 0; i < MAX_CLIENTS; ++i){
		if(clients[i]){
			printf("\n %i --> %s \n", i, clients[i]->login);
			}
		}

  printf("\n---------------------------------------------------\n");
	pthread_mutex_unlock(&clients_mutex);
}


void *socketThread(void *arg){
  printf("%d. THREAD \n", client_number);

  Client *client = (Client *)arg;
  client_number++;

  int n;

  while(1){
    n = recv(client->sockfd , client_message , 2000 , 0);

    if(n < 1){
        break;
    }

    // printf("\nRECV: %s\n",client_message);

    char *token;
    char msg[MSG_SIZE];
    char delimiter[] = "++"; 
    char receiver[64];

    token = strtok(client_message, delimiter); // key word

    printf("\n>> %s >> ", token);

    if (strcmp(token, "MSG") == 0){
      token = strtok(NULL, delimiter);
      printf("FROM %s ", token);
      strcpy(msg, "++");
      strcat(msg, token);
      strcat(msg, ": ");

      token = strtok(NULL, delimiter);
      printf("TO %s ", token);
      strcpy(receiver, token);

      token = strtok(NULL, delimiter);
      printf("IS %s ", token);
      strcat(msg, token);
      strcat(msg, "++");
      
      // printf("ALL: FROM %s TO %s IS %s ", client->login, receiver, msg);

      if(strlen(client_message) > 0){
				send_message(msg, receiver);
      }
    }    

    else if (strcmp(token, "LOGIN") == 0){
      token = strtok(NULL, delimiter);
      strcpy(client->login, token);

      printf("**%s** LOGGED IN", client->login);

      print_users();
    }

    else if (strcmp(token, "LOGOUT") == 0){
      printf("**%s** LOGGED OUT \n\n", client->login);
      break;
    }

    else if (strcmp(token, "CHAT") == 0){
      token = strtok(NULL, delimiter);
      printf("%s WITH", token);

      token = strtok(NULL, delimiter);
      printf(" %s ", token);
    }

    printf("\n");

    sleep(1);
    // bzero(client_message, MSG_SIZE);
    memset(client_message, 0, MSG_SIZE);
    }

    printf("EXIT SOCKETTHREAD \n");
    close(client->sockfd);
    remove_client(client->uid);
    free(client);
    client_number--;

    print_users();

    pthread_exit(NULL);
}


int main(){
  int server_socket, client_socket;
  struct sockaddr_in server_addr;
  struct sockaddr_storage server_storage;
  socklen_t addr_size;

  pthread_t thread_id;

  //Create the socket. 
  server_socket = socket(PF_INET, SOCK_STREAM, 0);

  // Configure settings of the server address struct
  // Address family = Internet 
  server_addr.sin_family = AF_INET;

  //Set port number, using htons function to use proper byte order 
  server_addr.sin_port = htons(PORT);

  //Set IP address to localhost 
  server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
  server_addr.sin_addr.s_addr = inet_addr(HOST);

  //Set all bits of the padding field to 0 
  memset(server_addr.sin_zero, '\0', sizeof server_addr.sin_zero);
  
  //Bind the address struct to the socket 
  bind(server_socket, (struct sockaddr *) &server_addr, sizeof(server_addr));

  //Listen on the socket
  if(listen(server_socket,50)==0)
    printf("Listening on port %i\n\n", PORT);
  else
    printf("ERROR: Listening failed\n");


  while(1){
      //Accept call creates a new socket for the incoming connection
      addr_size = sizeof server_storage;
      client_socket = accept(server_socket, (struct sockaddr *) &server_storage, &addr_size);

      if((client_number + 1) == MAX_CLIENTS){
        printf("Maximum number of clients! \n");
        close(client_socket);
        continue;
      }

      Client *client = (Client *)malloc(sizeof(Client));
      client->address = server_storage;
      client->sockfd = client_socket;
      client->uid = uid++;

      add_client(client);

      if( pthread_create(&thread_id, NULL, socketThread, (void*)client) != 0 )
          printf("Failed to create thread\n");

      pthread_detach(thread_id);
      pthread_join(thread_id,NULL);
  }

  return EXIT_SUCCESS;
}