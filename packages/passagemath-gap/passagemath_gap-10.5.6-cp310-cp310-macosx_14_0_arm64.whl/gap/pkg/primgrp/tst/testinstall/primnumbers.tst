gap> START_TEST("primnumbers.tst");
gap> Sum(List([1..4095],NrPrimitiveGroups));
24558
gap> List([1..4095],NrPrimitiveGroups);
[ 0, 1, 2, 2, 5, 4, 7, 7, 11, 9, 8, 6, 9, 4, 6, 22, 10, 4, 8, 4, 9, 4, 7, 5, 
  28, 7, 15, 14, 8, 4, 12, 7, 4, 2, 6, 22, 11, 4, 2, 8, 10, 4, 10, 4, 9, 2, 
  6, 4, 40, 9, 2, 3, 8, 4, 8, 9, 5, 2, 6, 9, 14, 4, 8, 74, 13, 7, 10, 7, 2, 
  2, 10, 4, 16, 4, 2, 2, 4, 6, 10, 4, 155, 10, 6, 6, 6, 2, 2, 2, 10, 4, 10, 
  2, 2, 2, 2, 2, 14, 4, 2, 38, 11, 5, 10, 4, 11, 2, 6, 4, 14, 4, 2, 10, 12, 
  4, 2, 2, 5, 2, 4, 23, 57, 7, 2, 2, 45, 19, 15, 7, 4, 7, 10, 4, 3, 2, 5, 14, 
  10, 4, 10, 4, 2, 2, 2, 17, 2, 2, 2, 2, 8, 4, 14, 4, 6, 2, 3, 9, 14, 4, 2, 
  2, 2, 7, 12, 4, 7, 2, 6, 9, 75, 7, 6, 2, 8, 4, 6, 6, 2, 2, 6, 4, 20, 4, 4, 
  2, 2, 3, 2, 2, 2, 6, 10, 4, 16, 4, 2, 10, 11, 4, 14, 4, 2, 2, 3, 2, 2, 2, 
  2, 5, 2, 6, 18, 4, 2, 2, 2, 22, 2, 2, 2, 5, 2, 2, 10, 4, 12, 2, 6, 4, 14, 
  4, 6, 2, 10, 6, 2, 2, 2, 2, 10, 4, 22, 4, 36, 6, 2, 2, 2, 3, 2, 2, 10, 4, 
  9, 2, 4, 244, 15, 4, 2, 2, 2, 2, 6, 4, 2, 3, 2, 2, 8, 4, 18, 4, 8, 2, 4, 8, 
  14, 4, 2, 24, 18, 4, 10, 4, 3, 4, 2, 2, 97, 7, 2, 2, 8, 4, 2, 2, 4, 2, 2, 
  11, 2, 2, 2, 2, 2, 2, 15, 4, 2, 2, 10, 4, 18, 4, 5, 2, 8, 4, 2, 2, 2, 2, 2, 
  10, 14, 2, 2, 2, 2, 6, 18, 4, 2, 2, 2, 9, 22, 4, 2, 2, 4, 2, 90, 8, 2, 2, 
  6, 4, 14, 4, 11, 2, 14, 4, 2, 2, 7, 2, 6, 20, 92, 7, 2, 11, 2, 2, 10, 4, 5, 
  2, 2, 2, 14, 4, 2, 2, 2, 11, 18, 4, 4, 2, 6, 4, 2, 2, 2, 2, 8, 4, 2, 2, 2, 
  2, 2, 4, 20, 4, 2, 16, 17, 4, 2, 2, 2, 6, 2, 2, 18, 4, 2, 2, 2, 2, 2, 7, 2, 
  2, 10, 4, 26, 4, 2, 2, 3, 2, 2, 2, 2, 2, 10, 4, 22, 4, 6, 2, 2, 2, 10, 4, 
  24, 2, 10, 4, 2, 2, 2, 2, 16, 4, 2, 2, 2, 2, 4, 4, 18, 4, 2, 2, 14, 8, 18, 
  4, 7, 2, 6, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 6, 4, 2, 2, 2, 10, 2, 2, 14, 
  4, 2, 2, 14, 4, 2, 2, 10, 12, 2, 2, 10, 4, 2, 2, 6, 8, 2, 3, 2, 2, 8, 4, 3, 
  58, 14, 2, 2, 2, 2, 2, 2, 9, 18, 4, 14, 4, 8, 2, 4, 9, 65, 7, 2, 2, 2, 2, 
  2, 2, 2, 2, 2, 10, 26, 4, 2, 2, 2, 2, 18, 4, 2, 2, 2, 2, 3, 2, 2, 2, 8, 4, 
  2, 6, 4, 2, 6, 4, 2, 2, 7, 2, 10, 4, 18, 4, 2, 3, 2, 11, 23, 4, 2, 2, 2, 2, 
  2, 2, 6, 2, 6, 4, 2, 2, 2, 2, 12, 4, 4, 2, 2, 2, 10, 4, 26, 4, 2, 2, 2, 2, 
  10, 4, 2, 2, 2, 2, 20, 4, 2, 4, 18, 4, 10, 5, 2, 2, 2, 2, 698, 10, 2, 2, 2, 
  4, 26, 4, 2, 2, 2, 2, 2, 2, 2, 2, 18, 4, 10, 4, 2, 2, 10, 4, 2, 2, 7, 2, 8, 
  4, 2, 2, 4, 2, 10, 9, 26, 4, 2, 2, 2, 6, 2, 2, 2, 2, 4, 8, 26, 4, 2, 30, 
  11, 4, 2, 4, 2, 2, 10, 4, 2, 2, 2, 2, 2, 2, 18, 4, 6, 2, 2, 2, 2, 2, 2, 2, 
  20, 4, 6, 2, 2, 2, 2, 2, 14, 4, 2, 2, 2, 2, 4, 2, 2, 2, 6, 4, 2, 2, 2, 2, 
  2, 2, 14, 4, 501, 15, 2, 2, 14, 4, 2, 2, 2, 2, 14, 4, 4, 2, 10, 4, 2, 2, 2, 
  2, 2, 3, 18, 4, 2, 2, 2, 7, 28, 4, 3, 2, 18, 4, 2, 2, 4, 2, 2, 2, 20, 4, 2, 
  2, 8, 4, 3, 2, 2, 2, 2, 4, 3, 2, 2, 38, 2, 2, 10, 4, 2, 2, 2, 4, 2, 2, 2, 
  2, 8, 4, 2, 2, 2, 2, 2, 2, 2, 10, 2, 2, 10, 4, 22, 4, 2, 2, 2, 4, 2, 2, 8, 
  24, 14, 4, 10, 4, 2, 2, 10, 4, 20, 4, 2, 2, 2, 2, 2, 2, 2, 2, 6, 8, 116, 7, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 4, 2, 2, 10, 4, 18, 4, 6, 2, 6, 4, 2, 2, 
  2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 14, 4, 2, 3, 22, 4, 20, 4, 2, 2, 6, 4, 2, 2, 
  6, 2, 2, 2, 2, 2, 2, 2, 2, 10, 2, 2, 6, 2, 2, 2, 10, 4, 2, 5, 18, 4, 2, 2, 
  2, 2, 2, 2, 18, 4, 2, 2, 2, 2, 2, 2, 2, 2, 14, 4, 2, 2, 2, 2, 2, 2, 26, 4, 
  2, 2, 14, 4, 2, 2, 4, 6, 10, 4, 2, 2, 2, 2, 18, 4, 2, 2, 2, 2, 2, 10, 134, 
  7, 2, 2, 2, 2, 18, 4, 4, 2, 10, 4, 2, 2, 2, 2, 12, 4, 2, 4, 2, 2, 6, 4, 2, 
  2, 2, 2, 2, 4, 26, 4, 4, 2, 2, 2, 14, 4, 2, 107, 4, 2, 2, 2, 2, 2, 2, 9, 
  32, 4, 2, 2, 14, 4, 3, 2, 2, 2, 6, 4, 26, 4, 4, 115, 8, 2, 2, 2, 2, 2, 10, 
  4, 18, 4, 4, 2, 2, 2, 10, 7, 2, 2, 2, 2, 3, 2, 2, 2, 10, 4, 26, 4, 2, 2, 2, 
  2, 4, 2, 2, 2, 14, 4, 14, 4, 2, 7, 2, 2, 14, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 
  11, 6, 2, 2, 2, 3, 2, 10, 4, 10, 2, 10, 9, 27, 4, 2, 2, 10, 4, 2, 6, 2, 2, 
  10, 4, 7, 2, 4, 2, 8, 4, 2, 2, 2, 2, 2, 2, 20, 4, 2, 16, 2, 2, 18, 4, 2, 2, 
  2, 6, 18, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  14, 4, 26, 4, 2, 6, 2, 2, 2, 2, 2, 2, 10, 4, 2, 2, 2, 2, 2, 2, 26, 4, 2, 2, 
  2, 11, 2, 2, 2, 2, 14, 4, 2, 2, 2, 2, 6, 4, 2, 2, 2, 2, 10, 4, 2, 2, 2, 2, 
  2, 2, 32, 4, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 14, 4, 2, 2, 16, 4, 2, 2, 2, 2, 
  10, 4, 23, 2, 2, 2, 8, 4, 18, 4, 2, 2, 2, 2, 14, 4, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 2, 26, 4, 2, 2, 2, 2, 2, 2, 2, 2, 10, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 4, 2, 14, 4, 14, 4, 2, 2, 6, 4, 2, 2, 4, 4, 18, 4, 18, 4, 2, 2, 
  2, 135, 27, 4, 2, 2, 20, 4, 18, 4, 2, 2, 6, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 6, 6, 34, 4, 2, 2, 2, 4, 18, 4, 2, 4, 92, 10, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 22, 4, 2, 2, 14, 
  2, 6, 4, 142, 7, 2, 2, 14, 4, 2, 2, 2, 6, 2, 2, 26, 4, 2, 2, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 2, 4, 2, 2, 2, 10, 4, 2, 2, 2, 2, 2, 2, 4, 6, 18, 4, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 4, 2, 2, 10, 4, 26, 4, 6, 2, 10, 4, 3, 2, 2, 
  2, 6, 4, 2, 2, 2, 10, 2, 2, 10, 4, 2, 2, 14, 4, 20, 4, 2, 5, 2, 2, 16, 4, 
  2, 2, 3, 8, 2, 2, 2, 2, 2, 2, 26, 4, 2, 2, 2, 2, 2, 2, 2, 2, 18, 4, 18, 4, 
  4, 2, 6, 4, 22, 4, 2, 2, 8, 4, 2, 2, 2, 2, 10, 4, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 2, 10, 4, 2, 2, 2, 2, 2, 2, 2, 2, 6, 2, 6, 4, 2, 2, 2, 2, 2, 2, 26, 4, 
  2, 2, 2, 2, 2, 2, 2, 7, 2, 2, 10, 4, 2, 2, 2, 2, 20, 9, 2, 2, 12, 4, 2, 2, 
  2, 2, 10, 4, 2, 2, 2, 2, 2, 2, 18, 4, 2, 2, 10, 4, 2, 2, 8, 2, 2, 2, 10, 4, 
  2, 2, 10, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 6, 26, 4, 2, 22, 23, 4, 2, 2, 
  2, 2, 10, 4, 18, 4, 2, 2, 14, 4, 2, 2, 2, 2, 6, 4, 32, 4, 2, 2, 2, 2, 10, 
  4, 2, 2, 2, 4, 2, 2, 2, 2, 8, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  4, 2, 2, 2, 26, 4, 2, 2, 2, 2, 10, 4, 2, 2, 14, 4, 14, 4, 2, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 194, 7, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 20, 4, 2, 2, 14, 4, 10, 
  4, 2, 2, 2, 2, 2, 2, 2, 2, 14, 4, 7, 2, 2, 2, 2, 6, 2, 2, 2, 2, 18, 4, 19, 
  4, 2, 2, 2, 26, 2, 2, 2, 2, 8, 4, 2, 2, 2, 2, 2, 2, 26, 4, 2, 2, 2, 2, 14, 
  4, 2, 6, 2, 2, 18, 4, 4, 2, 2, 2, 10, 4, 2, 2, 2, 10, 2, 2, 2, 2, 2, 6, 6, 
  2, 2, 2, 2, 2, 22, 4, 2, 2, 2, 4, 22, 4, 5, 2, 10, 4, 14, 4, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 4, 38, 4, 2, 2, 2, 2, 2, 2, 2, 2, 10, 4, 2, 2, 2, 2, 2, 2, 2, 
  4, 2, 2, 6, 4, 2, 2, 2, 2, 2, 6, 18, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 2, 10, 4, 132, 7, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 26, 4, 2, 2, 2, 2, 10, 
  4, 2, 2, 18, 4, 32, 4, 2, 2, 14, 4, 10, 4, 2, 2, 2, 2, 2, 2, 2, 2, 14, 4, 
  7, 2, 4, 2, 2, 2, 2, 2, 2, 2, 20, 4, 2, 2, 2, 2, 6, 4, 2, 2, 2, 2, 10, 4, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10, 4, 26, 4, 2, 10, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 8, 4, 26, 4, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 4, 2, 2, 2, 2, 10, 4, 2, 2, 2, 2, 2, 2, 10, 
  4, 2, 2, 2, 2, 18, 4, 2, 2, 8, 4, 18, 4, 2, 4, 18, 4, 2, 2, 2, 2, 2, 2, 18, 
  4, 2, 2, 4, 20, 38, 4, 2, 2, 2, 2, 2, 5, 36, 2, 6, 4, 20, 4, 2, 2, 2, 2, 2, 
  2, 2, 2, 6, 4, 2, 2, 2, 2, 2, 2, 3, 14, 4, 2, 2, 2, 26, 4, 2, 2, 2, 4, 2, 
  2, 2, 2, 6, 4, 2, 2, 2, 2, 14, 4, 2, 2, 2, 2, 2, 2, 2, 2, 4, 19, 26, 4, 10, 
  4, 2, 2, 10, 4, 26, 4, 2, 2, 2, 2, 2, 2, 2, 2, 6, 4, 2, 2, 2, 2, 2, 7, 4, 
  2, 4, 2, 10, 4, 30, 4, 2, 6, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 22, 4, 18, 
  4, 2, 2, 2, 2, 18, 4, 2, 2, 14, 4, 26, 4, 4, 2, 2, 2, 2, 2, 2, 2, 10, 4, 2, 
  2, 2, 2, 2, 2, 42, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 20, 
  4, 2, 2, 2, 2, 2, 2, 73, 6, 2, 2, 2, 2, 2, 2, 2, 2, 172, 8, 2, 2, 2, 2, 10, 
  4, 2, 2, 6, 4, 76, 7, 6, 2, 14, 4, 2, 2, 2, 2, 2, 2, 26, 4, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 4, 10, 4, 2, 2, 10, 4, 2, 2, 2, 2, 2, 2, 26, 
  4, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10, 4, 32, 4, 2, 2, 14, 4, 2, 
  2, 2, 6, 2, 2, 34, 4, 2, 2, 2, 2, 14, 4, 2, 2, 2, 2, 14, 4, 4, 2, 18, 4, 2, 
  5, 2, 2, 2, 12, 2, 2, 2, 2, 8, 4, 34, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 4, 2, 2, 2, 2, 10, 4, 38, 4, 2, 2, 2, 4, 18, 
  4, 2, 2, 14, 4, 2, 2, 2, 2, 14, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 18, 
  4, 2, 2, 2, 2, 34, 4, 2, 11, 26, 4, 10, 4, 2, 2, 2, 2, 14, 4, 2, 2, 18, 4, 
  2, 2, 2, 2, 10, 4, 1178, 10, 2, 2, 2, 2, 2, 2, 2, 2, 10, 4, 2, 2, 4, 2, 12, 
  4, 2, 2, 2, 2, 10, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 26, 4, 2, 4, 18, 
  4, 2, 2, 2, 2, 6, 9, 2, 2, 6, 2, 2, 2, 2, 2, 4, 2, 6, 4, 2, 2, 2, 2, 4, 2, 
  14, 4, 2, 2, 2, 2, 18, 4, 2, 2, 8, 4, 2, 2, 2, 2, 2, 2, 6, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 34, 2, 2, 14, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 2, 11, 50, 4, 2, 2, 2, 2, 2, 2, 2, 2, 18, 4, 2, 2, 2, 2, 2, 2, 
  18, 4, 2, 2, 10, 4, 2, 2, 2, 2, 20, 4, 26, 4, 2, 2, 2, 6, 20, 4, 2, 2, 2, 
  4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 6, 4, 2, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 18, 4, 32, 4, 2, 2, 2, 2, 2, 4, 6, 2, 2, 2, 2, 2, 2, 2, 12, 4, 
  2, 2, 2, 2, 2, 2, 18, 4, 2, 2, 14, 4, 2, 2, 2, 2, 2, 6, 2, 2, 2, 2, 18, 4, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 26, 4, 2, 2, 2, 2, 2, 2, 2, 2, 14, 4, 
  10, 4, 2, 2, 10, 4, 2, 2, 3, 2, 2, 2, 18, 4, 2, 2, 2, 2, 14, 4, 2, 2, 2, 2, 
  14, 4, 2, 2, 10, 4, 34, 4, 2, 2, 8, 4, 2, 2, 2, 2, 10, 4, 6, 2, 2, 9, 2, 2, 
  18, 4, 4, 2, 10, 4, 18, 4, 2, 2, 2, 2, 14, 4, 2, 2, 2, 2, 2, 2, 2, 2, 18, 
  4, 34, 4, 2, 2, 2, 2, 2, 2, 2, 2, 14, 4, 2, 22, 2, 2, 2, 2, 14, 4, 2, 12, 
  16, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10, 4, 2, 2, 2, 2, 2, 2, 4, 2, 
  10, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 4, 26, 4, 4, 2, 2, 2, 14, 4, 2, 2, 
  33, 4, 10, 4, 2, 2, 2, 4, 112, 7, 2, 2, 2, 2, 2, 2, 2, 2, 6, 4, 2, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 2, 22, 4, 10, 2, 8, 4, 2, 2, 2, 2, 14, 4, 2, 2, 2, 2, 
  2, 9, 26, 4, 2, 2, 2, 2, 34, 4, 2, 2, 26, 4, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 6, 4, 2, 2, 2, 2, 2, 2, 18, 4, 2, 2, 2, 2, 2, 2, 2, 2, 
  12, 4, 2, 2, 2, 2, 6, 4, 2, 2, 2, 2, 8, 4, 2, 2, 2, 2, 2, 10, 23, 4, 2, 2, 
  2, 2, 2, 2, 6, 5, 18, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10, 4, 2, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 2, 26, 4, 2, 2, 8, 4, 2, 2, 2, 2, 6, 4, 2, 2, 2, 2, 
  18, 4, 34, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 6, 4, 34, 4, 8, 2, 2, 2, 2, 2, 2, 2, 18, 4, 2, 2, 2, 2, 
  2, 2, 10, 4, 2, 2, 6, 4, 18, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 26, 4, 2, 2, 
  26, 4, 2, 2, 2, 2, 2, 2, 18, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 38, 4, 2, 2, 
  2, 2, 18, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 22, 4, 6, 2, 10, 4, 2, 2, 2, 2, 
  12, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 26, 4, 2, 2, 
  2, 2, 2, 2, 2, 2, 6, 4, 42, 4, 2, 2, 122, 6, 2, 2, 2, 2, 2, 2, 2, 2, 2, 34, 
  23, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 6, 2, 
  2, 18, 4, 2, 2, 6, 4, 38, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 26, 4, 2, 2, 2, 
  2, 18, 4, 2, 2, 18, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 6, 4, 2, 2, 2, 2, 10, 
  4, 2, 2, 2, 2, 2, 2, 22, 4, 2, 2, 26, 4, 2, 2, 2, 2, 2, 2, 14, 4, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 19, 2, 2, 2, 2, 2, 2, 2, 2, 11, 2, 18, 4, 14, 4, 2, 2, 
  18, 4, 14, 4, 2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 18, 4, 2, 2, 2, 9, 2, 2, 2, 8, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10, 4, 38, 4, 2, 2, 
  2, 2, 18, 4, 2, 2, 4, 2, 32, 4, 2, 2, 2, 2, 18, 4, 19, 2, 10, 4, 2, 2, 2, 
  2, 20, 4, 26, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10, 4, 2, 2, 10, 4, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 10, 4, 50, 4, 2, 6, 2, 2, 2, 2, 2, 2, 10, 4, 14, 4, 
  26, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 20, 4, 18, 4, 2, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 6, 2, 2, 2, 10, 4, 2, 2, 2, 2, 8, 4, 2, 2, 2, 2, 2, 7, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 34, 4, 2, 2, 2, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  10, 4, 2, 2, 2, 2, 2, 2, 34, 4, 2, 2, 14, 4, 10, 4, 2, 2, 6, 4, 20, 4, 2, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 94, 7, 2, 2, 2, 6, 2, 2, 2, 2, 10, 4, 2, 2, 2, 
  2, 2, 2, 18, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 34, 4, 2, 2, 2, 2, 14, 4, 2, 
  4, 2, 2, 2, 2, 2, 2, 10, 4, 38, 4, 2, 2, 8, 4, 2, 2, 2, 2, 10, 4, 27, 4, 2, 
  2, 2, 2, 14, 4, 2, 2, 2, 2, 2, 2, 2, 2, 14, 4, 10, 4, 2, 2, 2, 2, 2, 2, 2, 
  2, 2, 4, 34, 4, 2, 2, 2, 2, 2, 2, 2, 2, 14, 4, 14, 4, 2, 2, 2, 2, 2, 2, 2, 
  2, 10, 4, 2, 2, 2, 2, 2, 39, 2, 2, 2, 2, 2, 2, 10, 4, 2, 2, 2, 2, 26, 4, 2, 
  2, 14, 4, 2, 2, 2, 2, 6, 4, 2, 2, 2, 2, 2, 2, 26, 4, 2, 2, 2, 2, 20, 4, 2, 
  6, 2, 2, 10, 4, 2, 2, 2, 11, 2, 2, 2, 2, 2, 4, 4, 2, 2, 2, 10, 4, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 10, 4, 34, 4, 2, 2, 8, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 2, 2, 26, 4, 2, 2, 2, 2, 42, 4, 2, 2, 20, 4, 2, 2, 2, 2, 2, 2, 20, 4, 2, 
  2, 2, 2, 2, 2, 2, 2, 14, 4, 238, 7, 2, 2, 2, 2, 22, 4, 2, 2, 2, 2, 14, 4, 
  2, 2, 2, 2, 18, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 22, 4, 2, 2, 2, 2, 10, 4, 18, 4, 2, 2, 2, 2, 2, 2, 2, 2, 6, 4, 2, 2, 4, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 22, 4, 3, 2, 14, 4, 2, 2, 2, 2, 6, 4, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 4, 26, 4, 2, 2, 2, 4, 2, 2, 2, 
  2, 10, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10, 2, 2, 10, 4, 2, 4, 26, 4, 20, 4, 
  2, 2, 2, 2, 2, 2, 2, 2, 6, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 26, 4, 2, 
  2, 18, 4, 2, 2, 2, 2, 2, 4, 32, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 2, 10, 26, 4, 2, 2, 18, 4, 2, 2, 2, 6, 14, 4, 10, 4, 2, 2, 10, 4, 2, 2, 
  2, 2, 10, 4, 18, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 18, 4, 2, 2, 6, 4, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10, 4, 16, 2, 2, 2, 2, 2, 
  2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 8, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  4, 26, 4, 18, 4, 6, 2, 6, 4, 2, 2, 2, 2, 14, 4, 2, 2, 2, 2, 14, 4, 26, 4, 
  2, 2, 2, 2, 18, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 22, 4, 32, 4, 2, 2, 2, 2, 26, 4, 2, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 
  2, 10, 4, 2, 2, 2, 2, 6, 12, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 10, 4, 26, 4, 6 ]
gap> ForAll( [1..1000], n -> NrPrimitiveGroups( n ) =
>                            Length( AllPrimitiveGroups( NrMovedPoints, n )));
true
gap> ForAll( [1001..2000], n -> NrPrimitiveGroups( n ) =
>                            Length( AllPrimitiveGroups( NrMovedPoints, n )));
true
gap> ForAll( [2001..3000], n -> NrPrimitiveGroups( n ) =
>                            Length( AllPrimitiveGroups( NrMovedPoints, n )));
true
gap> ForAll( [3001..4000], n -> NrPrimitiveGroups( n ) =
>                            Length( AllPrimitiveGroups( NrMovedPoints, n )));
true
gap> ForAll( [4001..4095], n -> NrPrimitiveGroups( n ) =
>                            Length( AllPrimitiveGroups( NrMovedPoints, n )));
true
gap> STOP_TEST( "primnumbers.tst", 1);
