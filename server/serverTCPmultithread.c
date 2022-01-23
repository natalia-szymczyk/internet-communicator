#include<stdio.h>
#include<stdlib.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<string.h>
#include <arpa/inet.h>
#include <fcntl.h> // for open
#include <unistd.h> // for close
#include<pthread.h>

// gcc -g -Wall -pthread yourcode.c -lpthread -o yourprogram

#define PORT 8885
#define MAX_CLIENTS 100
#define MSG_SIZE 2048

char client_message[MSG_SIZE];
char user_list[30][50];
unsigned int client_number = 0;
char buffer[MSG_SIZE];
static int uid = 10;

pthread_mutex_t clients_mutex = PTHREAD_MUTEX_INITIALIZER;


/* Client structure */
typedef struct{
	struct sockaddr_storage address;
	int sockfd;
	int uid;
	char name[32];
} client_t;

client_t *clients[MAX_CLIENTS];


/* Send message to all clients except sender */
void send_message(char *s, char* name){
	pthread_mutex_lock(&clients_mutex);

	for(int i=0; i<MAX_CLIENTS; ++i){
		if(clients[i]){
			if(strcmp(clients[i]->name, name) == 0 ){
        if(send(clients[i]->sockfd, s, strlen(s), 0) < 0){
          perror("ERROR: write to descriptor failed");
          break;
        }
      }
			
		}
	}

	pthread_mutex_unlock(&clients_mutex);
}

void queue_add(client_t *cl){
	pthread_mutex_lock(&clients_mutex);

	for(int i = 0; i < MAX_CLIENTS; ++i){
		if(!clients[i]){
			clients[i] = cl;
			break;
		}
	}

	pthread_mutex_unlock(&clients_mutex);
}

void queue_remove(int uid){
	pthread_mutex_lock(&clients_mutex);

	for(int i=0; i < MAX_CLIENTS; ++i){
		if(clients[i]){
			if(clients[i]->uid == uid){
				clients[i] = NULL;
				break;
			}
		}
	}

	pthread_mutex_unlock(&clients_mutex);
}

void print_users(){
	pthread_mutex_lock(&clients_mutex);

	for(int i=0; i < MAX_CLIENTS; ++i){
		if(clients[i]){
			printf("\n %i --> %s \n", i, clients[i]->name);
			}
		}

	pthread_mutex_unlock(&clients_mutex);
}


void * socketThread(void *arg){
  printf("%d. THREAD \n", client_number);
  client_t *cli = (client_t *)arg;

  client_number++;

  int n;

  for(;;){
    n = recv(cli->sockfd , client_message , 2000 , 0);
    printf("RECV: %s\n",client_message);
        if(n < 1){
            break;
        }

    char *token;
    char msg[MSG_SIZE];
    char delimiter[] = "++"; 
    char receiver[64];

    char *message = malloc(MSG_SIZE);
    strcpy(message,client_message);

    token = strtok(message, delimiter); // slowo klucz

    printf(">> %s >> ", token);

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
      printf("IS %s \n", token);
      strcat(msg, token);
      strcat(msg, "++");

      // send(cli->sockfd,msg,MSG_SIZE,0);
      
      printf("ALL: FROM %s TO %s IS %s ", cli->name, receiver, msg);

      // send_message(msg ,cli->uid);

      if(strlen(client_message) > 0){
				// send_message(client_message, receiver);
				send_message(msg, receiver);
      }


      // send(cli->sockfd,message,MSG_SIZE,0);
    }
    else if (strcmp(token, "LOGIN") == 0){
      token = strtok(NULL, delimiter);
      strcpy(cli->name, token);

      printf("**%s** LOGGED IN", cli->name);

      print_users();
    }
    else if (strcmp(token, "LOGOUT") == 0){
      printf("**%s** LOGGED OUT \n", cli->name);
      break;
    }

    printf("\n");

    sleep(1);
    // send(newSocket,message,sizeof(message),0);
    // memset(&client_message, 0, MSG_SIZE);
    bzero(client_message, MSG_SIZE);

    }

    printf("EXIT SOCKETTHREAD \n");
    close(cli->sockfd);
    queue_remove(cli->uid);
    free(cli);
    client_number--;

    pthread_exit(NULL);

    // TODO segmentation fault kiedy wszystkie watki sie rozlaczaja
}


int main(){
  int serverSocket, newSocket;
  struct sockaddr_in serverAddr;
  struct sockaddr_storage serverStorage;
  socklen_t addr_size;

  //Create the socket. 
  serverSocket = socket(PF_INET, SOCK_STREAM, 0);

  // Configure settings of the server address struct
  // Address family = Internet 
  serverAddr.sin_family = AF_INET;

  //Set port number, using htons function to use proper byte order 
  serverAddr.sin_port = htons(PORT);

  //Set IP address to localhost 
  serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);


  //Set all bits of the padding field to 0 
  memset(serverAddr.sin_zero, '\0', sizeof serverAddr.sin_zero);
  
  // active users
  memset(user_list, 0, sizeof user_list);

  //Bind the address struct to the socket 
  bind(serverSocket, (struct sockaddr *) &serverAddr, sizeof(serverAddr));

  //Listen on the socket
  if(listen(serverSocket,50)==0)
    printf("Listening\n");
  else
    printf("Error\n");

    pthread_t thread_id;

  while(1){
      //Accept call creates a new socket for the incoming connection
      addr_size = sizeof serverStorage;
      newSocket = accept(serverSocket, (struct sockaddr *) &serverStorage, &addr_size);

      if((client_number + 1) == MAX_CLIENTS){
        printf("Max clients reached. Rejected: ");
        close(newSocket);
        continue;
      }

      client_t *cli = (client_t *)malloc(sizeof(client_t));
      cli->address = serverStorage;
      cli->sockfd = newSocket;
      cli->uid = uid++;

      queue_add(cli);

      if( pthread_create(&thread_id, NULL, socketThread, (void*)cli) != 0 )
          printf("Failed to create thread\n");

      pthread_detach(thread_id);
      pthread_join(thread_id,NULL);
  }
  return 0;
}
