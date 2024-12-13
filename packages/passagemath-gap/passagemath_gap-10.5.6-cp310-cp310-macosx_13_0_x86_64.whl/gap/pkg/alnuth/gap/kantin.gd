#############################################################################
##
#W kantin.gd        Alnuth - ALgebraic NUmber THeory           Bettina Eick
#W                                                           Bjoern Assmann
#W                                                          Andreas Distler
##

#############################################################################
##
#F PolynomialWithNameToStringList( f[, name] )
##
DeclareGlobalFunction("PolynomialWithNameToStringList");

#############################################################################
##
#F CoefficientsToStringList( name, coeffs )
##
DeclareGlobalFunction("CoefficientsToStringList");

#############################################################################
##
#F MaximalOrderDescriptionPari( F )
##
DeclareGlobalFunction("MaximalOrderDescriptionPari");

#############################################################################
##
#F UnitGroupDescriptionPari( F )
##
DeclareGlobalFunction("UnitGroupDescriptionPari");

#############################################################################
##
#F ExponentsOfUnitsDescriptionWithRankPari( F, elms )
##
DeclareGlobalFunction("ExponentsOfUnitsDescriptionWithRankPari");

#############################################################################
##
#F ExponentsOfFractionalIdealDescriptionPari(F, elms)
##
## <elms> are arbitrary elements of F (or rather their coefficients).
## Returns the exponents vectors of the fractional ideals
## generated by elms corresponding to the underlying prime ideals.
##
DeclareGlobalFunction("ExponentsOfFractionalIdealDescriptionPari"); 

#############################################################################
##
#F NormCosetsDescriptionPari(F, norm)
##
DeclareGlobalFunction("NormCosetsDescriptionPari");

#############################################################################
##
#F  PolynomialFactorsDescriptionPari, function( <F>, <coeffs> )
##
##  Factorizes the polynomial defined by <coeffs> over the field <F>
##  using PARI/GP
##
DeclareGlobalFunction( "PolynomialFactorsDescriptionPari" );

#############################################################################
##
#F ProcessPariGP(input, codefile)
##
DeclareGlobalFunction("ProcessPariGP");

#############################################################################
##
#E