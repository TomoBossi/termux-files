#include <stdlib.h>
#include <stdio.h>
#include <ncurses.h>
#include <sys/ioctl.h>

char d[] = {' ', '.', '-', '+', 'x', 'X', 'A', 'G', '#', '@'};
int n = sizeof(d)/sizeof(char);

int main(void) {
    initscr(); // init ncurses mode
    curs_set(0); // hide cursor
    start_color(); // enable color print
    init_pair(1, COLOR_GREEN, COLOR_BLACK); // green on black
    init_pair(2, COLOR_WHITE, COLOR_WHITE); // white on white
    init_pair(3, COLOR_GREEN, COLOR_GREEN); // green on green
	timeout(65); // sleep duration (ms)

    struct winsize s;
    ioctl(0, TIOCGWINSZ, &s);
    int w = s.ws_col; // terminal width
    int h = s.ws_row; // terminal height

    int m[h][w] = {};
    while (1) {
        for (int j = h-1; j >= 0; j--) {
            for (int i = w-1; i >= 0; i--) {
                if (j == 0 && rand() % 15 < 1) {
                    m[j][i] = n-1;
                }

                if (j < h-1) {
                    m[j+1][i] = m[j][i];
                }

                if (m[j][i] != n-1) {
                    attron(COLOR_PAIR(1));
                    if (m[j][i] > 0 && rand() % 10000 < 1) {
                        attron(COLOR_PAIR(3));
                    }
                } else {
                    attron(A_BOLD);
                    if (rand() % 30 < 1) {
                        attron(COLOR_PAIR(2));
                    }
                }

                mvprintw(j, i, "%c", d[m[j][i] <= 0 ? 0 : m[j][i]]); // print at row j, col i
                m[j][i]--;

                attroff(A_BOLD);
                attroff(COLOR_PAIR(1));
                attroff(COLOR_PAIR(2));
				attroff(COLOR_PAIR(3));
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
