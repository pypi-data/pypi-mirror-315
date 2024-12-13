gap> START_TEST("bugfix.tst");  

#
gap> m :=
> [ [ [ 1, 0, 0 ], [ 0, 1, 0 ], [ 0, 0, -1 ] ], 
>  [ [ 1, 0, 0 ], [ 0, -1, 0 ], [ 0, 0, 1 ] ], 
>  [ [ -1, 0, 0 ], [ 0, -1, 0 ], [ 0, 0, 1 ] ], 
>  [ [ 1, 0, 0 ], [ 0, 1, 0 ], [ 0, 0, -1 ] ], 
>  [ [ -1, 0, 0 ], [ 0, 1, 0 ], [ 0, 0, 1 ] ] ];;
gap> M := Group(m);
<matrix group with 5 generators>
gap> matrix := [ [ -1, 0, 0 ], [ 0, 1, 0 ], [ 0, 0, 1 ] ];
[ [ -1, 0, 0 ], [ 0, 1, 0 ], [ 0, 0, 1 ] ]
gap> IsomorphismPcpGroup(M);
[ [ [ -1, 0, 0 ], [ 0, -1, 0 ], [ 0, 0, 1 ] ], 
  [ [ 1, 0, 0 ], [ 0, 1, 0 ], [ 0, 0, -1 ] ], 
  [ [ -1, 0, 0 ], [ 0, 1, 0 ], [ 0, 0, 1 ] ] ] -> [ g1, g2, g3 ]

# GitHub issue #2: an error in IsomorphismPcpGroup
gap> G := Group(Z(7)^0 *
>    [ [ [ Z(7), 0, 0, 0, 0, 0, 0, 0 ],
>        [ 0, Z(7), 0, 0, 0, 0, 0, 0 ],
>        [ 0, 0, Z(7), 0, 0, 0, 0, 0 ],
>        [ 0, 0, 0, Z(7), 0, 0, 0, 0 ],
>        [ 0, 0, 0, 0, Z(7), 0, 0, 0 ],
>        [ 0, 0, 0, 0, 0, Z(7), 0, 0 ],
>        [ 0, 0, 0, 0, 0, 0, Z(7), 0 ],
>        [ 0, 0, 0, 0, 0, 0, 0, Z(7) ] ],
>    [ [ 0, 0, 0, 0, Z(7)^5, 0, 0, 0 ],
>        [ 0, 0, 0, 0, 0, Z(7)^5, 0, 0 ],
>        [ 0, 0, 0, 0, 0, 0, Z(7)^5, 0 ],
>        [ 0, 0, 0, 0, 0, 0, 0, Z(7)^5 ],
>        [ Z(7)^2, 0, 0, 0, 0, 0, 0, 0 ],
>        [ 0, Z(7)^2, 0, 0, 0, 0, 0, 0 ],
>        [ 0, 0, Z(7)^2, 0, 0, 0, 0, 0 ],
>        [ 0, 0, 0, Z(7)^2, 0, 0, 0, 0 ] ],
>    [ [ 0, 0, 0, 0, Z(7)^4, 0, 0, 0 ],
>        [ 0, 0, 0, 0, 0, Z(7)^4, 0, 0 ],
>        [ 0, 0, 0, 0, 0, 0, Z(7)^4, 0 ],
>        [ 0, 0, 0, 0, 0, 0, 0, Z(7)^4 ],
>        [ Z(7), 0, 0, 0, 0, 0, 0, 0 ],
>        [ 0, Z(7), 0, 0, 0, 0, 0, 0 ],
>        [ 0, 0, Z(7), 0, 0, 0, 0, 0 ],
>        [ 0, 0, 0, Z(7), 0, 0, 0, 0 ] ],
>    [ [ 0, 0, 0, 0, 0, 0, 0, Z(7)^5 ],
>        [ 0, 0, 0, 0, 0, 0, Z(7)^2, 0 ],
>        [ 0, 0, 0, 0, 0, Z(7)^5, 0, 0 ],
>        [ 0, 0, 0, 0, Z(7)^2, 0, 0, 0 ],
>        [ 0, 0, 0, Z(7)^2, 0, 0, 0, 0 ],
>        [ 0, 0, Z(7)^5, 0, 0, 0, 0, 0 ],
>        [ 0, Z(7)^2, 0, 0, 0, 0, 0, 0 ],
>        [ Z(7)^5, 0, 0, 0, 0, 0, 0, 0 ] ],
>    [ [ 0, Z(7), 0, 0, 0, 0, 0, 0 ],
>        [ Z(7)^4, 0, 0, 0, 0, 0, 0, 0 ],
>        [ 0, 0, 0, Z(7)^4, 0, 0, 0, 0 ],
>        [ 0, 0, Z(7), 0, 0, 0, 0, 0 ],
>        [ 0, 0, 0, 0, 0, Z(7), 0, 0 ],
>        [ 0, 0, 0, 0, Z(7)^4, 0, 0, 0 ],
>        [ 0, 0, 0, 0, 0, 0, 0, Z(7)^4 ],
>        [ 0, 0, 0, 0, 0, 0, Z(7), 0 ] ],
>    [ [ 0, 1, 0, 0, 0, 0, 0, 0 ],
>        [ Z(7)^3, 0, 0, 0, 0, 0, 0, 0 ],
>        [ 0, 0, 0, Z(7)^3, 0, 0, 0, 0 ],
>        [ 0, 0, 1, 0, 0, 0, 0, 0 ],
>        [ 0, 0, 0, 0, 0, 1, 0, 0 ],
>        [ 0, 0, 0, 0, Z(7)^3, 0, 0, 0 ],
>        [ 0, 0, 0, 0, 0, 0, 0, Z(7)^3 ],
>        [ 0, 0, 0, 0, 0, 0, 1, 0 ] ],
>    [ [ 0, 0, 0, 0, Z(7)^4, 0, 0, 0 ],
>        [ 0, 0, 0, 0, 0, Z(7)^4, 0, 0 ],
>        [ 0, 0, 0, 0, 0, 0, Z(7)^4, 0 ],
>        [ 0, 0, 0, 0, 0, 0, 0, Z(7)^4 ],
>        [ Z(7)^4, 0, 0, 0, 0, 0, 0, 0 ],
>        [ 0, Z(7)^4, 0, 0, 0, 0, 0, 0 ],
>        [ 0, 0, Z(7)^4, 0, 0, 0, 0, 0 ],
>        [ 0, 0, 0, Z(7)^4, 0, 0, 0, 0 ] ],
>    [ [ Z(7)^4, 0, 0, 0, 0, 0, 0, 0 ],
>        [ 0, Z(7)^4, 0, 0, 0, 0, 0, 0 ],
>        [ 0, 0, Z(7), 0, 0, 0, 0, 0 ],
>        [ 0, 0, 0, Z(7), 0, 0, 0, 0 ],
>        [ 0, 0, 0, 0, Z(7)^4, 0, 0, 0 ],
>        [ 0, 0, 0, 0, 0, Z(7)^4, 0, 0 ],
>        [ 0, 0, 0, 0, 0, 0, Z(7), 0 ],
>        [ 0, 0, 0, 0, 0, 0, 0, Z(7) ] ],
>    [ [ Z(7)^2, 0, 0, 0, 0, 0, 0, 0 ],
>        [ 0, Z(7)^5, 0, 0, 0, 0, 0, 0 ],
>        [ 0, 0, Z(7)^2, 0, 0, 0, 0, 0 ],
>        [ 0, 0, 0, Z(7)^5, 0, 0, 0, 0 ],
>        [ 0, 0, 0, 0, Z(7)^2, 0, 0, 0 ],
>        [ 0, 0, 0, 0, 0, Z(7)^5, 0, 0 ],
>        [ 0, 0, 0, 0, 0, 0, Z(7)^2, 0 ],
>        [ 0, 0, 0, 0, 0, 0, 0, Z(7)^5 ] ],
>    [ [ Z(7)^2, 0, 0, 0, 0, 0, 0, 0 ],
>        [ 0, Z(7)^2, 0, 0, 0, 0, 0, 0 ],
>        [ 0, 0, Z(7)^2, 0, 0, 0, 0, 0 ],
>        [ 0, 0, 0, Z(7)^2, 0, 0, 0, 0 ],
>        [ 0, 0, 0, 0, Z(7)^2, 0, 0, 0 ],
>        [ 0, 0, 0, 0, 0, Z(7)^2, 0, 0 ],
>        [ 0, 0, 0, 0, 0, 0, Z(7)^2, 0 ],
>        [ 0, 0, 0, 0, 0, 0, 0, Z(7)^2 ] ],
>    [ [ 0, Z(7), 0, Z(7)^4, 0, Z(7), 0, Z(7)^4 ],
>        [ Z(7), 0, Z(7), 0, Z(7), 0, Z(7), 0 ],
>        [ 0, Z(7)^4, 0, Z(7), 0, Z(7), 0, Z(7)^4 ],
>        [ Z(7)^4, 0, Z(7)^4, 0, Z(7), 0, Z(7), 0 ],
>        [ Z(7)^4, 0, Z(7), 0, Z(7), 0, Z(7)^4, 0 ],
>        [ 0, Z(7), 0, Z(7), 0, Z(7)^4, 0, Z(7)^4 ],
>        [ Z(7), 0, Z(7)^4, 0, Z(7), 0, Z(7)^4, 0 ],
>        [ 0, Z(7)^4, 0, Z(7)^4, 0, Z(7)^4, 0, Z(7)^4 ] ],
>    [ [ 1, Z(7)^3, Z(7)^3, 1, Z(7)^3, 1, 1, Z(7)^3 ],
>        [ Z(7)^3, 1, Z(7)^3, 1, 1, Z(7)^3, 1, Z(7)^3 ],
>        [ Z(7)^3, Z(7)^3, Z(7)^3, Z(7)^3, Z(7)^3, Z(7)^3, Z(7)^3, Z(7)^3 ],
>        [ 1, 1, Z(7)^3, Z(7)^3, 1, 1, Z(7)^3, Z(7)^3 ],
>        [ Z(7)^3, 1, Z(7)^3, 1, Z(7)^3, 1, Z(7)^3, 1 ],
>        [ 1, Z(7)^3, Z(7)^3, 1, 1, Z(7)^3, Z(7)^3, 1 ],
>        [ 1, 1, Z(7)^3, Z(7)^3, Z(7)^3, Z(7)^3, 1, 1 ],
>        [ Z(7)^3, Z(7)^3, Z(7)^3, Z(7)^3, 1, 1, 1, 1 ] ],
>    [ [ 0, Z(7)^4, 0, Z(7), Z(7)^4, 0, Z(7), 0 ],
>        [ Z(7)^4, 0, Z(7)^4, 0, 0, Z(7), 0, Z(7) ],
>        [ 0, Z(7)^4, 0, Z(7), Z(7), 0, Z(7)^4, 0 ],
>        [ Z(7)^4, 0, Z(7)^4, 0, 0, Z(7)^4, 0, Z(7)^4 ],
>        [ Z(7), 0, Z(7)^4, 0, 0, Z(7)^4, 0, Z(7) ],
>        [ 0, Z(7), 0, Z(7), Z(7), 0, Z(7), 0 ],
>        [ Z(7)^4, 0, Z(7), 0, 0, Z(7)^4, 0, Z(7) ],
>        [ 0, Z(7)^4, 0, Z(7)^4, Z(7), 0, Z(7), 0 ] ] ]);
<matrix group with 13 generators>
gap> iso := IsomorphismPcpGroup(G);; # this
gap> Size(Image(iso));
16128
gap> Image(iso);
Pcp-group with orders [ 3, 2, 3, 7, 2, 2, 2, 2, 2, 2, 2 ]

#
gap> STOP_TEST( "bugfix.tst", 100000);
