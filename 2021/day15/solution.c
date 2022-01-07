#include <stdio.h>
#include <limits.h>
#include <stdlib.h>

#if 1
#define SIZE 10
#define INPUT "test_input.dat"
#else
#define SIZE 100
#define INPUT "input.dat"
#endif

#define MULTIPLIER 5
#define ARRAY_SIZE 10

static int size = SIZE;

int get_xy(int x, int y)
{
	if (x < 0 || y < 0 || x >= size || y >= size)
		return -1;

	return y * size + x;
}

int get_x(int xy)
{
	return xy % size;
}

int get_y(int xy)
{
	int mod = xy % size;
	return (xy - mod) / size;
}

void init_grid(int *grid, int size, int value)
{
	for (int i = 0; i < size; i ++) {
		grid[i] = value;
	}
}

void grow_grid(int *grid)
{

}

void load_grid(int *grid)
{
	char c;
	int i = 0;
	FILE *file = fopen(INPUT, "r");
	if (file) {
		while ((c = getc(file)) != EOF) {
			if (c != '\n')
				grid[i++] = c - 48;
		}
		fclose(file);
	}
}

void print_grid(int *grid, int xmax, int ymax, int d_size)
{
	for (int y = 0; y < ymax; y++) {
		for (int x = 0; x < xmax; x++) {
			printf("%3d", *(grid + get_xy(x, y)));
		}
		printf("\n");
	}
}

void print_list(int *list, int count)
{
	for (int i = 0; i < count; i++) {
		printf("%d", list[i]);
		printf("%s", i==count-1 ? "\n" : ", ");
	}
}

int *resize_array(int *arr, int orig_size)
{
	// Always double
	int *new_arr = malloc(orig_size * 2 * sizeof(int));
	// init_grid(new_arr, orig_size * 2, -1);
	printf("Resizing array from %d to %d\n", orig_size, orig_size * 2);
	for (int i = 0; i < orig_size; i++) {
		printf("Assigning %d and %d\n", i, orig_size + i);
		new_arr[i] = arr[i];
		new_arr[orig_size + i] = -1;
	}

	printf("Freeing original array, and assingning new one\n");
	return new_arr;
}

int clean_and_get_next(int *list, int array_size, int clean, int* distance) {
	int cleaned = 0;
	int cleaning = 0;
	int i = 0;
	int dist = INT_MAX;
	int next = -1;
	while (i < array_size && !cleaned) {
		if (list[i] == clean)
			cleaning = 1;
		else if (list[i] != -1 && distance[list[i]] < dist) {
			next = list[i];
			dist = distance[next];
		}

		if (cleaning)
			list[i] = list[i+1];
		
		if (list[i] == -1)
			cleaned = 1;
		
		i++;
	}
	if (i == array_size && list[i-1] != -1)
		list[i-1] = -1;
	return next;
}

int get_shortest_route_dijkstra(int *grid, int xi, int yi, int xf, int yf)
{

	int visited[size * size];
	init_grid(visited, size * size, 0);
	int distance[size * size];
	init_grid(distance, size * size, INT_MAX);

	int xy = get_xy(xi, yi);
	int x = xi;
	int y = xi;

	distance[xy] = 0;

	int array_size = ARRAY_SIZE;

	int *unvisited = malloc(array_size * sizeof(int));
	init_grid(unvisited, array_size, -1);
	int unvisited_count = 1;
	unvisited[0] = xy;

	int idx_final = get_xy(xf, yf);
	printf("Final: (%d, %d)[%d]\n", xf, yf, idx_final);
	while (distance[idx_final] == INT_MAX) {
		visited[xy] = 1;
		// Update adjacents, if not visited yet, add to list of unvisited

		printf("Visiting (%d, %d)[%d], distance: %d\n", x, y, xy, distance[xy]);
		printf("Unvisited list size: %d:\t\t", unvisited_count);
		print_list(unvisited, array_size);

		for (int i = 0; i < 4; i++) {
			int xa = x;
			int ya = y;
			if (i == 0) {
				xa = x - 1;
			}
			else if (i == 1) {
				ya = y - 1;
			}
			else if (i == 2) {
				xa = x + 1;
			} else {
				ya = y + 1;
			}
			printf("i = %d\t", i);
			int xya = get_xy(xa, ya);
			printf("\tChecking adjacent (%d, %d)[%d], current distance: %d, visited: %d\n", xa, ya, xya, distance[xya], visited[xya]);
			
			if (xya == -1)
				continue;

			if (visited[xya])
				continue;

			int new_dist = distance[xy] += grid[xya];
			int old_dist = distance[xya];
			if (old_dist == INT_MAX) {
				unvisited[unvisited_count++] = xya;
				if (unvisited_count == array_size) {
					int *new_arr = resize_array(unvisited, array_size);
					free(unvisited);
					unvisited = new_arr;
					array_size *= 2;
				}
			}

			if (new_dist < old_dist)
				distance[xya] = new_dist;
		}
		xy = clean_and_get_next(unvisited, unvisited_count, xy, distance);
		x = get_x(xy);
		y = get_y(xy);
		unvisited_count--;
	}

	print_grid(distance, size, size, 3);

	return distance[idx_final];
}

int part1()
{
	int grid[size * size];
	load_grid(grid);
	return get_shortest_route_dijkstra(grid, 0, 0, size - 1, size - 1);
}

int part2()
{
	return 0;
	size = MULTIPLIER * SIZE;
	int grid[size * size];
	init_grid(grid, size*size, 0);
	grow_grid(grid);
	return get_shortest_route_dijkstra(grid, 0, 0, size - 1, size - 1);
}

int main()
{
	printf("\n\n---------------------------------------------------------------\n");
	printf("Part1: %d\nPart2: %d\n", part1(), part2());
	printf("---------------------------------------------------------------\n");
}
