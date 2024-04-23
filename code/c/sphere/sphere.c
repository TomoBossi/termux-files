#include <stdlib.h>
#include <stdio.h>
#include <ncurses.h>
#include <sys/ioctl.h>
#include <string.h>

typedef struct vec3 { 
    double x;
	double y;
	double z;
} vec3;

double dot(vec3 a, vec3 b) {
	return a.x*b.x + a.y*b.y + a.z*b.z;
}

vec3 cross(vec3 a, vec3 b) {
	vec3 n;	
	n.x = a.y*b.z - a.z*b.y;
	n.y = - a.x*b.z + a.z*b.x;
	n.z = a.x*b.y - a.y*b.x;
	return n;
}

vec3 s_intersect(vec3 ray, double r) {
	vec3 i;
	i.x = 0.0;
	i.y = 0.0;
	i.z = 0.0;
	return i;
}

int main(void) {
    initscr(); // init ncurses mode
    curs_set(0); // hide cursor
	timeout(25); // sleep duration (ms)

    struct winsize s;
    ioctl(0, TIOCGWINSZ, &s);
    int w = s.ws_col, h = s.ws_row; // terminal width and height

	char m[] = " .:;^+=szXG&@";
	int n = (sizeof(m) - 1)/sizeof(char);
	double r = w > h ? h/2.5 : w/2.5;
	double f = 0.2;
	double d = 1.0;
	while (1) {
    	for (int j = h-h/2-1; j >= -h/2; j--) {
            for (int i = w-w/2-1; i >= -w/2; i--) { 

				if (j*j + f*i*i < r*r) {
                	mvprintw(j+h/2, i+w/2, "%c", m[(i+w/2)*n/w]);
				} else {
					mvprintw(j+h/2, i+w/2, "%c", m[j > 0 && j%2? j/2*n/h : 0]);
				}
            }
        }
        refresh(); // clear
        int c = getch();
        if (c == ' ') {
            break;
        }
    }
    endwin(); // end ncurses mode
    return 0;
}

