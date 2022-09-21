// Othello Implemented in C
// 20305003 Uzair

// **READ**

/* BOARD LAYOUT

   1 2 3 4 5 6 7 8
10 . . . . . . . .
20 . . . . . . . .
30 . . . . . . . .
40 . . . W B . . .
50 . . . B W . . .
60 . . . . . . . .
70 . . . . . . . .
80 . . . . . . . .

****In this case if you are going first and you want to place your piece at (60,6) then you will enter "66" as your input***
*/

#include <stdlib.h>
#include <stdio.h>

// 4 board positions, 4 values
const int empty = 0;
const int outer = 3;
const int black = 1;
const int white = 2;


const int directions[8]={-11, -10, -9, -1, 1, 9, 10, 11};
const int boardsize=100;


int humanInput (int user, int * brd);
int computerInput(int user, int * brd);

// Store the options for each user. Each user can either play themselves or have a computer play in their place
void * allStrats[3][3] = {
        {"human", "human", humanInput},
        {"computer", "computer", computerInput},
        {NULL, NULL, NULL}
};

// This function will assign each player to a certain colour using a switch case
// If the current player is black(1), then the opponent will be white(2) and vice versa
int colourDecider (int user) {
    switch (user) {
        case 1: return 2;
        case 2: return 1;
    }
}

// This function will create the starting/inital board with all spaces empty except for 2 black and 2 white pieces in the center
int * startingBoard(void){
    int i, * brd;
    brd = (int *)malloc(boardsize * sizeof(int));

    for (i = 0; i<=9; i++){
        brd[i]=outer;
    }

    for (i = 10; i<=89; i++){
        if (i%10 >= 1 && i%10 <= 8){
            brd[i]=empty;
        }
        else{
            brd[i]=outer;
        }
    }

    for (i = 90; i<=99; i++){
        brd[i]=outer;
        brd[44]=white;
        brd[45]=black;
        brd[54]=black;
        brd[55]=white;
    }
    return brd;
}

// Each square can only either be a white piece(W) or a black piece(B)
char options (int piece) {
    static char piecenames[4] = ".BW";
    return(piecenames[piece]);
}

// This is a simple counting function that will count how many pieces each player has on the current board
int pieceCounter (int user, int * brd) {
    int i, count;
    count=0;
    for (i=1; i<=88; i++){
        if (brd[i] == user){
            count++;
        }
    }
    return count;
}

// This function will print out the board along with the location of all pieces occupied on the board by each player
// The function pieceCounter is called here and will display the total number of pieces each player has on the board
// at that point in the game "[b=2 w=2]"
void printBoard (int * brd) {
    int row, column;
    printf("    1 2 3 4 5 6 7 8 [%c=%d  %c=%d]\n", options(black), pieceCounter(black, brd), options(white), pieceCounter(white, brd));
    for (row=1; row<=8; row++) {
        printf("%d  ", 10*row);
        for (column=1; column<=8; column++){
            printf("%c ", options(brd[column + (10 * row)]));
        }
        printf("\n");
    }
}

// This function ensures a player is making a valid move that is within the boundaries of the board
int validMove (int move) {
    if ((move >= 11) && (move <= 88) && (move%10 >= 1) && (move%10 <= 8)){
        return 1;
    }
    else{
        return 0;
    }
}

// This function will start from a square occupied by a player's opponent and advance in a direction past
// all opponent pieces until it finds a square occupied by the player.
// If a square held by the player is not identified until passing an empty or outer square, a 0 is returned.
int CorrespondingPiece(int square, int user, int * brd, int dir) {
    while (brd[square] == colourDecider(user)){
        square = square + dir;
    }
    if (brd[square] == user){
        return square;}
    else{
        return 0;
    }
}

// This function returns 2 squares from the board that are to be used by later functions, the square the current player is moving to, and
// a square that brackets an opponent piece
int flip (int move, int user, int * brd, int dir) {
    int z;
    z = move + dir;
    if (brd[z] == colourDecider(user)){
        return CorrespondingPiece(z+dir, user, brd, dir);
    }
    else{
        return 0;
    }
}

// This function will carry out all legal moves for both players aswell as flipping any pieces if necessary using the flip function
int legalMove (int move, int user, int * brd) {
    int i;
    if (!validMove(move)){
        return 0;
    }

    if (brd[move]==empty){
        i=0;
        while (i<=7 && !flip(move, user, brd, directions[i])){
            i++;
        }
        if (i==8){
            return 0;
        }
        else{
            return 1;
        }
    }
    else{
        return 0;
    }
}

// This function will flip all opponent pieces along a given direction once a player has decided on a move
void flipPieces (int move, int user, int * brd, int dir) {
    int flipCheck, z;
    flipCheck = flip(move, user, brd, dir);

    if (flipCheck){
        z = move + dir;
        do {
            brd[z] = user;
            z = z + dir;
        } while (z != flipCheck);
    }
}

// This function will place the pieces on the board on the location indicated by the player aswell as calling the flipPieces function to flip opponent pieces
void placePiece (int move, int user, int * brd) {
    int i;
    brd[move] = user;
    for (i=0; i<=7; i++){
        flipPieces(move, user, brd, directions[i]);
    }
}

// This function will check if a player has atleast one legal move and return 1 if so, otherwise return 0
int checkLegalMove (int user, int * brd) {
    int move;
    move = 11;

    while (move <= 88 && !legalMove(move, user, brd)){
        move++;
    }
    if (move <= 88){
        return 1;
    }
    else{
        return 0;
    }
}

// This function chooses the player whose move it will be next
int nextMove (int * brd, int previousplayer, int boardprint) {
    int opponent;
    opponent = colourDecider(previousplayer);

    if (checkLegalMove(opponent, brd)){
        return opponent;
    }
    if (checkLegalMove(previousplayer, brd)){
        if (boardprint){}
        printf("%c has no moves and must pass\n", options(opponent));
        return previousplayer;
    }
    return 0;
}

// This function is called to store all the legal moves a machine player can make in an array.
// This will be utilised later when the user is asked if they wish to print each board
// from a game between 2 computers
int * storeMoves (int user, int * brd) {
    int move, i, * totalMoves;
    totalMoves = (int *)malloc(65 * sizeof(int));
    totalMoves[0] = 0;
    i = 0;

    for (move=11; move<=88; move++){
        if (legalMove(move, user, brd)){
            i++;
            totalMoves[i]=move;
        }
    }
    totalMoves[0]=i;
    return totalMoves;
}

// This function gets the next move(input) from a human player
int humanInput (int user, int * brd) {
    int move;
    printf("%c's turn to move:", options(user));
    scanf("%d", &move);
    return move;
}

// This function will choose a random legal move from all the available moves for a machine player
int computerInput(int user, int * brd) {
    int r, * totalMoves;
    totalMoves = storeMoves(user, brd);
    r = totalMoves[(rand() % totalMoves[0]) + 1];
    free(totalMoves);
    return(r);
}

// This function gets a move from either user and carrys it out if it is a legal move, otherwise it will print an
// error to screen and allow the user to re-enter a move
void obtainMove (int (* strat) (int, int *), int user, int * brd, int boardprint) {
    int move;
    if (boardprint){
        printBoard(brd);
    }
    move = (* strat)(user, brd);

    if (legalMove(move, user, brd)) {
        if (boardprint) printf("%c has moved to %d\n", options(user), move);
        placePiece(move, user, brd);
    }
    else {
        printf("%d is an Illegal Move, Try Again\n", move);
        obtainMove(strat, user, brd, boardprint);
    }
}

// This function co-ordinates a game between both users and also informs when the game is over
void Othello (int (* blackStrat) (int, int *), int (* whiteStrat) (int, int *), int boardprint) {
    int user;
    user = black;

    int * brd;
    brd = startingBoard();
    do {
        if (user == black){
            obtainMove(blackStrat, black, brd, boardprint);
        }
        else{
            obtainMove(whiteStrat, white, brd, boardprint);
        }
        user = nextMove(brd, user, boardprint);
    }

    while (user != 0);
    // Print final board
    if (boardprint) {
        printf("\n***GAME OVER***\n\n");
        printBoard(brd);
    }
}

// This function will setup the game by asking each player whether they wish to play as a human or let the computer play in their place.
// It will then call the Othello function to begin carrying out the game. Also, if both players are computers it will print out all the boards
// from the game between the 2 computers including all moves they made
void setupGame (void) {
    char * choices;
    int i, user1, user2, boardprint;
    int (* stratUser1)(int, int *);
    int (* stratUser2)(int, int *);

    // Ask User 1 whether they wish to play manually or let the computer play for them
    i=0;
    printf("User 1: ");
    while (allStrats[i][0] != NULL) {
        choices=allStrats[i][1];
        printf("%d-%s\n", i, choices);
        printf("        ");
        i++;
    }
    printf(": ");
    scanf("%d", &user1);

    // Ask User 2 whether they wish to play manually or let the computer play for them
    i=0;
    printf("User 2: ");
    while (allStrats[i][0] != NULL) {
        choices=allStrats[i][1];
        printf("%d-%s\n", i, choices);
        printf("        ");
        i++;
    }
    printf(": ");
    scanf("%d", &user2);


    stratUser1 = allStrats[user1][2];
    stratUser2 = allStrats[user2][2];

    // Print each board if both players are human
    if (stratUser1 == humanInput || stratUser2 == humanInput){
        boardprint = 1;
    }
        // If both players are not human it will print all the boards from the game between the 2 computers
    else {
        boardprint = 1;
    }

    Othello(stratUser1, stratUser2, boardprint);
}

// Main Function
int main (void) {
    do {
        setupGame();
        fflush(stdin);
        // Ask the user if they want to run the program again
        printf("Would you like to play another game? (y or n)? ");
    } while (getchar() == 'y');
}
