#include <stdlib.h>
#include <stdio.h>
#include <ncurses.h>
#include <sys/ioctl.h>

/* gcc -lncurses matrix.c */

char d[] = {' ', '.', '-', '+', 'x', 'X', 'A', 'G', '#', '@'};
int n = sizeof(d)/sizeof(char);

int idx(char e) {
    int m = n;
    while (m--) {
        if (d[m] == e) {
            return m;
        }
    }
    return -1;
}

char next(char e) {
    int i = idx(e);
    if (i > 0) {
        return d[i-1];
    }
    return d[0];
}

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

    char m[h][w];
    for (int j = 0; j < h; j++) {
        for (int i = 0; i < w; i++) {
            m[j][i] = d[0];
        }
    }

    m[0][10] = '@';
    while (1) {
        for (int j = h-1; j >= 0; j--) {
            for (int i = w-1; i >= 0; i--) {
                if (j == 0 && rand() % 15 < 1) {
                    m[j][i] = d[n-1];
                }

                if (j < h-1) {
                    m[j+1][i] = m[j][i];
                }

                if (m[j][i] != d[n-1]) {
                    attron(COLOR_PAIR(1));
                    if (m[j][i] != d[0] && rand() % 10000 < 1) {
                        attron(COLOR_PAIR(3));
                    }
                } else {
                    attron(A_BOLD);
                    if (rand() % 30 < 1) {
                        attron(COLOR_PAIR(2));
                    }
                }

                mvprintw(j, i, "%c", m[j][i]); // print at row j, col i
                m[j][i] = next(m[j][i]);

                attroff(A_BOLD);
                attroff(COLOR_PAIR(1));
                attroff(COLOR_PAIR(2));
		attroff(COLOR_PAIR(3));
            }
        }

        refresh(); // clear
    
        int c = getch();
        if ( c == ' ') {
            break;
        }
    }

    endwin(); // end ncurses mode
    return 0;
}
