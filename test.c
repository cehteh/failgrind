#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

void func()
{
  void* foo = malloc(10);

  printf("%p, %d, %s\n", foo, errno, strerror(errno));

  free(foo);
}


int main()
{
  int* foo = malloc(10);
  printf("%p, %d, %s\n", foo, errno, strerror(errno));
  *foo = 1234; // will crash on injection

  func();

  free(foo);
  return 0;
}

