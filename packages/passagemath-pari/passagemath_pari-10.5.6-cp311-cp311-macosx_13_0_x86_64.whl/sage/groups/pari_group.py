# sage_setup: distribution = sagemath-pari
# sage.doctest: needs sage.groups sage.libs.pari
r"""
PARI Groups

See :pari:`polgalois` for the PARI documentation of these objects.
"""

from sage.libs.pari import pari
from sage.misc.lazy_import import lazy_import
from sage.rings.integer import Integer

lazy_import('sage.groups.perm_gps.permgroup_named', 'TransitiveGroup')


class PariGroup:
    def __init__(self, x, degree):
        """
        EXAMPLES::

            sage: PariGroup([6, -1, 2, "S3"], 3)
            PARI group [6, -1, 2, S3] of degree 3
            sage: R.<x> = PolynomialRing(QQ)
            sage: f = x^4 - 17*x^3 - 2*x + 1
            sage: G = f.galois_group(pari_group=True); G
            PARI group [24, -1, 5, "S4"] of degree 4
        """
        self.__x = pari(x)
        self.__degree = Integer(degree)

    def __repr__(self):
        """
        String representation of this group.

        EXAMPLES::

            sage: PariGroup([6, -1, 2, "S3"], 3)
            PARI group [6, -1, 2, S3] of degree 3
        """
        return "PARI group %s of degree %s" % (self.__x, self.__degree)

    def __eq__(self, other):
        """
        Test equality.

        EXAMPLES::

            sage: R.<x> = PolynomialRing(QQ)
            sage: f1 = x^4 - 17*x^3 - 2*x + 1
            sage: f2 = x^3 - x - 1
            sage: G1 = f1.galois_group(pari_group=True)
            sage: G2 = f2.galois_group(pari_group=True)
            sage: G1 == G1
            True
            sage: G1 == G2
            False
        """
        return (isinstance(other, PariGroup) and
            (self.__x, self.__degree) == (other.__x, other.__degree))

    def __ne__(self, other):
        """
        Test inequality.

        EXAMPLES::

            sage: R.<x> = PolynomialRing(QQ)
            sage: f1 = x^4 - 17*x^3 - 2*x + 1
            sage: f2 = x^3 - x - 1
            sage: G1 = f1.galois_group(pari_group=True)
            sage: G2 = f2.galois_group(pari_group=True)
            sage: G1 != G1
            False
            sage: G1 != G2
            True
        """
        return not (self == other)

    def __pari__(self):
        """
        TESTS::

            sage: G = PariGroup([6, -1, 2, "S3"], 3)
            sage: pari(G)
            [6, -1, 2, S3]
        """
        return self.__x

    def degree(self):
        """
        Return the degree of this group.

        EXAMPLES::

            sage: R.<x> = PolynomialRing(QQ)
            sage: f1 = x^4 - 17*x^3 - 2*x + 1
            sage: G1 = f1.galois_group(pari_group=True)
            sage: G1.degree()
            4
        """
        return self.__degree

    def signature(self):
        """
        Return 1 if contained in the alternating group, -1 otherwise.

        EXAMPLES::

            sage: R.<x> = QQ[]
            sage: f1 = x^4 - 17*x^3 - 2*x + 1
            sage: G1 = f1.galois_group(pari_group=True)
            sage: G1.signature()
            -1
        """
        return Integer(self.__x[1])

    def transitive_number(self):
        """
        If the transitive label is nTk, return `k`.

        EXAMPLES::

            sage: R.<x> = QQ[]
            sage: f1 = x^4 - 17*x^3 - 2*x + 1
            sage: G1 = f1.galois_group(pari_group=True)
            sage: G1.transitive_number()
            5
        """
        return Integer(self.__x[2])

    def label(self):
        """
        Return the human readable description for this group generated by Pari.

        EXAMPLES::

            sage: R.<x> = QQ[]
            sage: f1 = x^4 - 17*x^3 - 2*x + 1
            sage: G1 = f1.galois_group(pari_group=True)
            sage: G1.label()
            'S4'
        """
        return str(self.__x[3])

    def order(self):
        """
        Return the order of ``self``.

        EXAMPLES::

            sage: R.<x> = PolynomialRing(QQ)
            sage: f1 = x^4 - 17*x^3 - 2*x + 1
            sage: G1 = f1.galois_group(pari_group=True)
            sage: G1.order()
            24
        """
        return Integer(self.__x[0])

    cardinality = order

    def permutation_group(self):
        """
        Return the corresponding GAP transitive group.

        EXAMPLES::

            sage: R.<x> = QQ[]
            sage: f = x^8 - x^5 + x^4 - x^3 + 1
            sage: G = f.galois_group(pari_group=True)
            sage: G.permutation_group()
            Transitive group number 44 of degree 8
        """
        return TransitiveGroup(self.__degree, self.__x[2])

    _permgroup_ = permutation_group
