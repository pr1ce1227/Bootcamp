#include <stdio.h>

int main(int argc, char *argv[])
{
    printf("%d\n\r\n", argc);
    printf("%d\n\r\n", argc);
    printf("%d\n\r\n", argc);
    printf("%d\n\r\n", argc);
    printf("%d\n\r\n", argc);
    myfunc();
    // This is a new idea
    return 0;
}

myfunc()
{
    printf("do something");
}