#include <iostream>
#include <fstream>
#include <string>
#define size 1000

int main(int argc, char *argv[]) {
    
    int maze[size][size] = {0}, solution[size][2] = {0};
    int x = 0, y = 0, direction = 0, n_sol = 0;
    int x_d, y_d, x_w, y_w, x_a, y_a, x_s, y_s;
    int n_row, n_col;
    std::string maze_file, solution_file;
    
    if (argc < 3) {
        std::cout << "Usage:" << std::endl;
        std::cout << "  ./mazesolver <maze file> <solution file>" << std::endl;
        return 0;
    }
    else {
        maze_file = argv[1];
        solution_file = argv[2];
    }
    
    // Read the maze data
    std::ifstream f(maze_file);
    
    if (f.is_open()) {
        f >> n_row >> n_col;
        if (n_row > size or n_col > size) {
            std::cout << "Not enough storage avaliable" << std::endl;
            return 0;
        }
        
        // -1 indicates the presence of wall
        while (f) {
            int i, j;
            f >> i >> j;
            maze[i][j] = -1;
        }
        
        // 1 indicates the road
        for (int i = 0; i < n_row; i++) {
            for (int j = 0; j < n_col; j++) {
                if (maze[i][j] != -1)
                    maze[i][j] = 1;
            }
        }
        f.close();
    }
    else {
        std::cout << "Failed to open input file" << std::endl;
        return 0;
    }
    
    // Find the maze entrance in the first row and initialize the current state:
    //   (1) x, y are the current position
    //   (2) direction is the current moving direction: 0 = down, 1 = left, 2 = up, 3 = right
    for (int j = 0; j < n_col; j++) {
        if (maze[0][j] == 1) {
            x = 0; y = j; direction = 0;
            solution[n_sol][0] = x;
            solution[n_sol][1] = y;
            n_sol++;
        }
    }
    
    // Before reach the last row, choose new moving direction by current state
    // Moving direction: d = turn right, w = move forward, a = turn left, s = move backward
    while (x != n_row - 1) {
        switch (direction) {
            case 0: x_d=x; y_d=y-1; x_w=x+1; y_w=y; x_a=x; y_a=y+1; x_s=x-1; y_s=y; break;
            case 1: x_d=x-1; y_d=y; x_w=x; y_w=y-1; x_a=x+1; y_a=y; x_s=x; y_s=y+1; break;
            case 2: x_d=x; y_d=y+1; x_w=x-1; y_w=y; x_a=x; y_a=y-1; x_s=x+1; y_s=y; break;
            default: x_d=x+1; y_d=y; x_w=x; y_w=y+1; x_a=x-1; y_a=y; x_s=x; y_s=y-1; break;
        }
        
        // Try 4 types of moving directions in order:
        //   Turn right -> Move forward -> Turn left -> Move backward
        if (maze[x_d][y_d] == 1) {
            direction = (direction + 1) % 4; x = x_d; y = y_d;
        }
        else if (maze[x_w][y_w] == 1) {
            x = x_w; y = y_w;
        }
        else if (maze[x_a][y_a] == 1) {
            direction = (direction + 3) % 4; x = x_a; y = y_a;
        }
        else {
            direction = (direction + 2) % 4; x = x_s; y = y_s;
        }
        
        // Store current postion to solution
        solution[n_sol][0] = x;
        solution[n_sol][1] = y;
        n_sol++;
    }
    
    // Write solution into file
    std::ofstream of(solution_file);
    
    if (of.is_open()) {
        for  (int i = 0; i < n_sol; i++)
            of << solution[i][0] << " " << solution[i][1] << std::endl;
        f.close();
    }
    else {
        std::cout << "Failed to open output file" << std::endl;
        return 0;
    }
    return 0;
}

