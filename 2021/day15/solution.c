#include <stdio.h>

#if 1
#define SIZE 10
#define INPUT "test_input.txt"
#else
#define SIZE 100
#define INPUT "input.txt"
#endif

static int multiplier = 1;


int get_xy(int x, int y)
{
	return y * (multiplier * SIZE) + x;
}

void init_grid(int **grid, int size, int value)
{
	for (int i = 0; i < size; i ++) {
		*grid[i] = value;
	}
}

void grow_grid()
{

}

int get_shortest_route_dijkstra(int **grid, int xi, int yi, int xf, int yf)
{
	return 0;
}



int part1()
{
	int grid[SIZE*SIZE];
	init_grid(&grid, SIZE*SIZE, 0);
	return get_shortest_route_dijkstra(0, 0, SIZE-1, SIZE-1);
}

int part2()
{
	multiplier = 5;
	grow_grid();
	return get_shortest_route_dijkstra(0, 0, (multiplier * SIZE) - 1, (multiplier * SIZE) - 1);
}

int main()
{
	printf("Part1: %d\nPart2: %d\n", part1(), part2());
}
