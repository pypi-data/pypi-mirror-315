# sage_setup: distribution = sagemath-combinat
# sage.doctest: needs sage.combinat sage.graphs sage.modules
"""
Crystals of Kac modules of the general-linear Lie superalgebra
"""

#*****************************************************************************
#       Copyright (C) 2017 Travis Scrimshaw <tcscrims at gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.structure.parent import Parent
from sage.structure.element_wrapper import ElementWrapper
from sage.structure.unique_representation import UniqueRepresentation
from sage.rings.integer_ring import ZZ

from sage.categories.regular_supercrystals import RegularSuperCrystals
from sage.combinat.crystals.tensor_product import CrystalOfTableaux
from sage.combinat.root_system.cartan_type import CartanType
from sage.combinat.partition import _Partitions


class CrystalOfOddNegativeRoots(UniqueRepresentation, Parent):
    r"""
    Crystal of the set of odd negative roots.

    Let `\mathfrak{g}` be the general-linear Lie superalgebra
    `\mathfrak{gl}(m|n)`. This is the crystal structure on the set of
    negative roots as given by [Kwon2012]_.

    More specifically, this is the crystal basis of the subalgebra
    of `U_q^-(\mathfrak{g})` generated by `f_{\alpha}`, where `\alpha`
    ranges over all odd positive roots. As `\QQ(q)`-modules, we have

    .. MATH::

        U_q^-(\mathfrak{g}) \cong
        K \otimes U^-_q(\mathfrak{gl}_m \oplus \mathfrak{gl}_n).

    EXAMPLES::

        sage: S = crystals.OddNegativeRoots(['A', [2,1]])
        sage: mg = S.module_generator(); mg
        {}
        sage: mg.f(0)
        {-e[-1]+e[1]}
        sage: mg.f_string([0,-1,0,1,2,1,0])
        {-e[-2]+e[3], -e[-1]+e[1], -e[-1]+e[2]}
    """
    @staticmethod
    def __classcall_private__(cls, cartan_type):
        """
        Normalize input to ensure a unique representation.

        TESTS::

            sage: S1 = crystals.OddNegativeRoots(['A', [2,1]])
            sage: S2 = crystals.OddNegativeRoots(CartanType(['A', [2,1]]))
            sage: S1 is S2
            True
        """
        return super().__classcall__(cls, CartanType(cartan_type))

    def __init__(self, cartan_type):
        """
        Initialize ``self``.

        TESTS::

            sage: S = crystals.OddNegativeRoots(['A', [2,1]])
            sage: TestSuite(S).run()
        """
        self._cartan_type = cartan_type
        Parent.__init__(self, category=RegularSuperCrystals())
        self.module_generators = (self.element_class(self, frozenset()),)

    def _repr_(self):
        """
        Return a string representation of ``self``.

        EXAMPLES::

            sage: crystals.OddNegativeRoots(['A', [2,1]])
            Crystal of odd negative roots of type ['A', [2, 1]]
        """
        return "Crystal of odd negative roots of type {}".format(self._cartan_type)

    def module_generator(self):
        """
        Return the module generator of ``self``.

        EXAMPLES::

            sage: S = crystals.OddNegativeRoots(['A', [2,1]])
            sage: S.module_generator()
            {}
        """
        return self.module_generators[0]

    class Element(ElementWrapper):
        """
        An element of the crystal of odd negative roots.

        TESTS:

        Check that `e_i` and `f_i` are psuedo-inverses::

            sage: S = crystals.OddNegativeRoots(['A', [2,1]])
            sage: for x in S:
            ....:     for i in S.index_set():
            ....:         y = x.f(i)
            ....:         assert y is None or y.e(i) == x

        Check that we obtain the entire powerset of negative odd roots::

            sage: S = crystals.OddNegativeRoots(['A', [2,3]])
            sage: S.cardinality()
            4096
            sage: 2^len(S.weight_lattice_realization().positive_odd_roots())
            4096
        """

        def _repr_(self):
            r"""
            Return a string representation of ``self``.

            EXAMPLES::

                sage: S = crystals.OddNegativeRoots(['A', [2,2]])
                sage: mg = S.module_generator(); mg
                {}
                sage: mg.f(0)
                {-e[-1]+e[1]}
                sage: mg.f_string([0,-1,0])
                {-e[-2]+e[1], -e[-1]+e[1]}
            """
            return ('{'
                    + ", ".join("-e[{}]+e[{}]".format(*i)
                                for i in sorted(self.value))
                    + '}')

        def _latex_(self):
            r"""
            Return a latex representation of ``self``.

            EXAMPLES::

                sage: S = crystals.OddNegativeRoots(['A', [2,2]])
                sage: mg = S.module_generator()
                sage: latex(mg)
                \{\}
                sage: latex(mg.f(0))
                \{-e_{-1}+e_{1}\}
                sage: latex(mg.f_string([0,-1,0]))
                \{-e_{-2}+e_{1}, -e_{-1}+e_{1}\}
            """
            return (r'\{'
                    + ", ".join("-e_{{{}}}+e_{{{}}}".format(*i)
                                for i in sorted(self.value))
                    + r'\}')

        def e(self, i):
            r"""
            Return the action of the crystal operator `e_i` on ``self``.

            EXAMPLES::

                sage: S = crystals.OddNegativeRoots(['A', [2,2]])
                sage: mg = S.module_generator()
                sage: mg.e(0)
                sage: mg.e(1)
                sage: b = mg.f_string([0,1,2,-1,0])
                sage: b.e(-1)
                sage: b.e(0)
                {-e[-2]+e[3]}
                sage: b.e(1)
                sage: b.e(2)
                {-e[-2]+e[2], -e[-1]+e[1]}
                sage: b.e_string([2,1,0,-1,0])
                {}
            """
            if i == 0:
                if (-1,1) not in self.value:
                    return None
                return type(self)(self.parent(), self.value.difference([(-1,1)]))

            count = 0
            act_val = None
            if i < 0:
                lst = sorted(self.value, key=lambda x: (x[1], -x[0]))
                for val in lst:
                    # We don't have to check val[1] because this is an odd root
                    if val[0] == i - 1:
                        if count == 0:
                            act_val = val
                        else:
                            count -= 1
                    elif val[0] == i:
                        count += 1
                if act_val is None:
                    return None
                ret = self.value.difference([act_val]).union([(i, act_val[1])])
                return type(self)(self.parent(), ret)

            # else i > 0
            lst = sorted(self.value, key=lambda x: (-x[0], -x[1]))
            for val in reversed(lst):
                # We don't have to check val[0] because this is an odd root
                if val[1] == i + 1:
                    if count == 0:
                        act_val = val
                    else:
                        count -= 1
                elif val[1] == i:
                    count += 1
            if act_val is None:
                return None
            ret = self.value.difference([act_val]).union([(act_val[0], i)])
            return type(self)(self.parent(), ret)

        def f(self, i):
            r"""
            Return the action of the crystal operator `f_i` on ``self``.

            EXAMPLES::

                sage: S = crystals.OddNegativeRoots(['A', [2,2]])
                sage: mg = S.module_generator()
                sage: mg.f(0)
                {-e[-1]+e[1]}
                sage: mg.f(1)
                sage: b = mg.f_string([0,1,2,-1,0]); b
                {-e[-2]+e[3], -e[-1]+e[1]}
                sage: b.f(-2)
                {-e[-3]+e[3], -e[-1]+e[1]}
                sage: b.f(-1)
                sage: b.f(0)
                sage: b.f(1)
                {-e[-2]+e[3], -e[-1]+e[2]}
            """
            if i == 0:
                if (-1,1) in self.value:
                    return None
                return type(self)(self.parent(), self.value.union([(-1,1)]))

            count = 0
            act_val = None
            if i < 0:
                lst = sorted(self.value, key=lambda x: (x[1], -x[0]))
                for val in reversed(lst):
                    # We don't have to check val[1] because this is an odd root
                    if val[0] == i:
                        if count == 0:
                            act_val = val
                        else:
                            count -= 1
                    elif val[0] == i - 1:
                        count += 1
                if act_val is None:
                    return None
                ret = self.value.difference([act_val]).union([(i-1, act_val[1])])
                return type(self)(self.parent(), ret)

            # else i > 0
            lst = sorted(self.value, key=lambda x: (-x[0], -x[1]))
            for val in lst:
                # We don't have to check val[0] because this is an odd root
                if val[1] == i:
                    if count == 0:
                        act_val = val
                    else:
                        count -= 1
                elif val[1] == i + 1:
                    count += 1
            if act_val is None:
                return None
            ret = self.value.difference([act_val]).union([(act_val[0], i+1)])
            return type(self)(self.parent(), ret)

        def epsilon(self, i):
            r"""
            Return `\varepsilon_i` of ``self``.

            EXAMPLES::

                sage: S = crystals.OddNegativeRoots(['A', [2,2]])
                sage: mg = S.module_generator()
                sage: [mg.epsilon(i) for i in S.index_set()]
                [0, 0, 0, 0, 0]
                sage: b = mg.f_string([0,1,0,-1,0,-1,-2,-2]); b
                {-e[-3]+e[1], -e[-3]+e[2], -e[-1]+e[1]}
                sage: [b.epsilon(i) for i in S.index_set()]
                [2, 0, 1, 0, 0]
                sage: b = mg.f_string([0,1,0,-1,0,-1,-2,-2,2,-1,0]); b
                {-e[-3]+e[1], -e[-3]+e[3], -e[-2]+e[1], -e[-1]+e[1]}
                sage: [b.epsilon(i) for i in S.index_set()]
                [1, 0, 1, 0, 1]

            TESTS::

                sage: S = crystals.OddNegativeRoots(['A', [2,1]])
                sage: def count_e(x, i):
                ....:     ret = -1
                ....:     while x is not None:
                ....:         x = x.e(i)
                ....:         ret += 1
                ....:     return ret
                sage: for x in S:
                ....:     for i in S.index_set():
                ....:         assert x.epsilon(i) == count_e(x, i)
            """
            if i == 0:
                return ZZ.one() if (-1,1) in self.value else ZZ.zero()

            count = 0
            ret = 0
            if i < 0:
                lst = sorted(self.value, key=lambda x: (x[1], -x[0]))
                for val in lst:
                    # We don't have to check val[1] because this is an odd root
                    if val[0] == i - 1:
                        if count == 0:
                            ret += 1
                        else:
                            count -= 1
                    elif val[0] == i:
                        count += 1

            else: # i > 0
                lst = sorted(self.value, key=lambda x: (-x[0], -x[1]))
                for val in reversed(lst):
                    # We don't have to check val[0] because this is an odd root
                    if val[1] == i + 1:
                        if count == 0:
                            ret += 1
                        else:
                            count -= 1
                    elif val[1] == i:
                        count += 1
            return ret

        def phi(self, i):
            r"""
            Return `\varphi_i` of ``self``.

            EXAMPLES::

                sage: S = crystals.OddNegativeRoots(['A', [2,2]])
                sage: mg = S.module_generator()
                sage: [mg.phi(i) for i in S.index_set()]
                [0, 0, 1, 0, 0]
                sage: b = mg.f(0)
                sage: [b.phi(i) for i in S.index_set()]
                [0, 1, 0, 1, 0]
                sage: b = mg.f_string([0,1,0,-1,0,-1]); b
                {-e[-2]+e[1], -e[-2]+e[2], -e[-1]+e[1]}
                sage: [b.phi(i) for i in S.index_set()]
                [2, 0, 0, 1, 1]

            TESTS::

                sage: S = crystals.OddNegativeRoots(['A', [2,1]])
                sage: def count_f(x, i):
                ....:     ret = -1
                ....:     while x is not None:
                ....:         x = x.f(i)
                ....:         ret += 1
                ....:     return ret
                sage: for x in S:
                ....:     for i in S.index_set():
                ....:         assert x.phi(i) == count_f(x, i)
            """
            if i == 0:
                return ZZ.zero() if (-1,1) in self.value else ZZ.one()

            count = 0
            ret = 0
            if i < 0:
                lst = sorted(self.value, key=lambda x: (x[1], -x[0]))
                for val in reversed(lst):
                    # We don't have to check val[1] because this is an odd root
                    if val[0] == i:
                        if count == 0:
                            ret += 1
                        else:
                            count -= 1
                    elif val[0] == i - 1:
                        count += 1

            else: # i > 0
                lst = sorted(self.value, key=lambda x: (-x[0], -x[1]))
                for val in lst:
                    # We don't have to check val[0] because this is an odd root
                    if val[1] == i:
                        if count == 0:
                            ret += 1
                        else:
                            count -= 1
                    elif val[1] == i + 1:
                        count += 1
            return ret

        def weight(self):
            r"""
            Return the weight of ``self``.

            EXAMPLES::

                sage: S = crystals.OddNegativeRoots(['A', [2,2]])
                sage: mg = S.module_generator()
                sage: mg.weight()
                (0, 0, 0, 0, 0, 0)
                sage: mg.f_string([0,1,2,-1,-2]).weight()
                (-1, 0, 0, 0, 0, 1)
                sage: mg.f_string([0,1,2,-1,-2,0,1,0,2]).weight()
                (-1, 0, -2, 1, 0, 2)

            TESTS::

                sage: S = crystals.OddNegativeRoots(['A', [2,1]])
                sage: al = S.weight_lattice_realization().simple_roots()
                sage: for x in S:
                ....:     for i in S.index_set():
                ....:         y = x.f(i)
                ....:         assert y is None or x.weight() - al[i] == y.weight()
            """
            WLR = self.parent().weight_lattice_realization()
            e = WLR.basis()
            return WLR.sum(-e[i]+e[j] for (i,j) in self.value)


class CrystalOfKacModule(UniqueRepresentation, Parent):
    r"""
    Crystal of a Kac module.

    Let `\mathfrak{g}` be the general linear Lie superalgebra
    `\mathfrak{gl}(m|n)`. Let `\lambda` and `\mu` be dominant weights
    for `\mathfrak{gl}_m` and `\mathfrak{gl}_n`, respectively.
    Let `K` be the module `K = \langle f_{\alpha} \rangle`,
    where `\alpha` ranges over all odd positive roots. A *Kac module*
    is the `U_q(\mathfrak{g})`-module constructed from the highest
    weight `U_q(\mathfrak{gl}_m \oplus \mathfrak{gl}_n)`-module
    `V(\lambda, \mu)` (induced to a `U_q(\mathfrak{g})`-module in
    the natural way) by

    .. MATH::

        K(\lambda, \mu) := K \otimes_L V(\lambda, \mu),

    where `L` is the subalgebra generated by `e_0` and
    `U_q(\mathfrak{gl}_m \oplus \mathfrak{gl}_n)`.

    The Kac module admits a `U_q(\mathfrak{g})`-crystal structure
    by taking the crystal structure of `K` as given by
    :class:`~sage.combinat.crystals.kac_modules.CrystalOfOddNegativeRoots`
    and the crystal `B(\lambda, \mu)` (the natural crystal structure
    of `V(\lambda, \mu)`).

    .. NOTE::

        Our notation differs slightly from [Kwon2012]_ in that our
        last tableau is transposed.

    EXAMPLES::

        sage: K = crystals.KacModule(['A', [1,2]], [2], [1,1])
        sage: K.cardinality()
        576
        sage: K.cardinality().factor()
        2^6 * 3^2
        sage: len(K.cartan_type().root_system().ambient_space().positive_odd_roots())
        6
        sage: mg = K.module_generator()
        sage: mg
        ({}, [[-2, -2]], [[1], [2]])
        sage: mg.weight()
        (2, 0, 1, 1, 0)
        sage: mg.f(-1)
        ({}, [[-2, -1]], [[1], [2]])
        sage: mg.f(0)
        ({-e[-1]+e[1]}, [[-2, -2]], [[1], [2]])
        sage: mg.f(1)
        sage: mg.f(2)
        ({}, [[-2, -2]], [[1], [3]])

        sage: sorted(K.highest_weight_vectors(), key=str)
        [({-e[-1]+e[3]}, [[-2, -1]], [[1], [2]]),
         ({-e[-1]+e[3]}, [[-2, -2]], [[1], [2]]),
         ({}, [[-2, -2]], [[1], [2]])]

    ::

        sage: K = crystals.KacModule(['A', [1,1]], [2], [1])
        sage: K.cardinality()
        96
        sage: K.cardinality().factor()
        2^5 * 3
        sage: len(K.cartan_type().root_system().ambient_space().positive_odd_roots())
        4

        sage: sorted(K.highest_weight_vectors(), key=str)
        [({-e[-1]+e[2]}, [[-2, -1]], [[1]]),
         ({-e[-1]+e[2]}, [[-2, -2]], [[1]]),
         ({}, [[-2, -2]], [[1]])]
        sage: K.genuine_lowest_weight_vectors()
        (({-e[-2]+e[1], -e[-2]+e[2], -e[-1]+e[1], -e[-1]+e[2]}, [[-1, -1]], [[2]]),)
        sage: sorted(K.lowest_weight_vectors(), key=str)
        [({-e[-1]+e[1], -e[-1]+e[2]}, [[-1, -1]], [[2]]),
         ({-e[-2]+e[1], -e[-2]+e[2], -e[-1]+e[1], -e[-1]+e[2]}, [[-1, -1]], [[2]]),
         ({-e[-2]+e[2], -e[-1]+e[1], -e[-1]+e[2]}, [[-1, -1]], [[1]]),
         ({-e[-2]+e[2], -e[-1]+e[1], -e[-1]+e[2]}, [[-1, -1]], [[2]])]

    REFERENCES:

    - [Kwon2012]_
    """
    @staticmethod
    def __classcall_private__(cls, cartan_type, la, mu):
        """
        Normalize input to ensure a unique representation.

        TESTS::

            sage: K1 = crystals.KacModule(['A', [2,1]], [2,1], [1])
            sage: K2 = crystals.KacModule(CartanType(['A', [2,1]]), (2,1), (1,))
            sage: K1 is K2
            True
        """
        cartan_type = CartanType(cartan_type)
        la = _Partitions(la)
        mu = _Partitions(mu)
        return super().__classcall__(cls, cartan_type, la, mu)

    def __init__(self, cartan_type, la, mu):
        """
        Initialize ``self``.

        TESTS::

            sage: K = crystals.KacModule(['A', [2,1]], [2,1], [1])
            sage: TestSuite(K).run()
        """
        self._cartan_type = cartan_type
        self._la = la
        self._mu = mu
        Parent.__init__(self, category=RegularSuperCrystals())
        self._S = CrystalOfOddNegativeRoots(self._cartan_type)
        self._dual = CrystalOfTableaux(['A', self._cartan_type.m], shape=la)
        self._reg = CrystalOfTableaux(['A', self._cartan_type.n], shape=mu)
        data = (self._S.module_generators[0],
                self._dual.module_generators[0],
                self._reg.module_generators[0])
        self.module_generators = (self.element_class(self, data),)

    def _repr_(self):
        r"""
        Return a string representation of ``self``.

        EXAMPLES::

            sage: crystals.KacModule(['A', [2,1]], [3,1], [1])
            Crystal of Kac module K([3, 1], [1]) of type ['A', [2, 1]]
        """
        return "Crystal of Kac module K({}, {}) of type {}".format(
                    self._la, self._mu, self._cartan_type)

    def module_generator(self):
        """
        Return the module generator of ``self``.

        EXAMPLES::

            sage: K = crystals.KacModule(['A', [2,1]], [2,1], [1])
            sage: K.module_generator()
            ({}, [[-3, -3], [-2]], [[1]])
        """
        return self.module_generators[0]

    class Element(ElementWrapper):
        r"""
        An element of a Kac module crystal.

        TESTS:

        Check that `e_i` and `f_i` are psuedo-inverses::

            sage: K = crystals.KacModule(['A', [2,1]], [2,1], [1])
            sage: for x in K:
            ....:     for i in K.index_set():
            ....:         y = x.f(i)
            ....:         assert y is None or y.e(i) == x
        """

        def _repr_(self):
            """
            Return a string representation of ``self``.

            EXAMPLES::

                sage: K = crystals.KacModule(['A', [2,1]], [2,1], [1])
                sage: mg = K.module_generator(); mg
                ({}, [[-3, -3], [-2]], [[1]])
                sage: mg.f_string([0,1,-2,1,-1,0,-1,-1,1,-2,-2])
                ({-e[-3]+e[2], -e[-1]+e[2]}, [[-2, -1], [-1]], [[2]])
            """
            return repr((self.value[0], to_dual_tableau(self.value[1]), self.value[2]))

        def _latex_(self):
            r"""
            Return a string representation of ``self``.

            EXAMPLES::

                sage: K = crystals.KacModule(['A', [2,1]], [2,1], [1])
                sage: mg = K.module_generator()
                sage: latex(mg)
                \{\}
                 \otimes {\def\lr#1{\multicolumn{1}{|@{\hspace{.6ex}}c@{\hspace{.6ex}}|}{\raisebox{-.3ex}{$#1$}}}
                \raisebox{-.6ex}{$\begin{array}[b]{*{2}c}\cline{1-2}
                \lr{\overline{3}}&\lr{\overline{3}}\\\cline{1-2}
                \lr{\overline{2}}\\\cline{1-1}
                \end{array}$}
                } \otimes {\def\lr#1{\multicolumn{1}{|@{\hspace{.6ex}}c@{\hspace{.6ex}}|}{\raisebox{-.3ex}{$#1$}}}
                \raisebox{-.6ex}{$\begin{array}[b]{*{1}c}\cline{1-1}
                \lr{1}\\\cline{1-1}
                \end{array}$}
                }
                sage: latex(mg.f_string([0,1,-2,1,-1,0,-1,-1,1,-2,-2]))
                \{-e_{-3}+e_{2}, -e_{-1}+e_{2}\}
                 \otimes {\def\lr#1{\multicolumn{1}{|@{\hspace{.6ex}}c@{\hspace{.6ex}}|}{\raisebox{-.3ex}{$#1$}}}
                \raisebox{-.6ex}{$\begin{array}[b]{*{2}c}\cline{1-2}
                \lr{\overline{2}}&\lr{\overline{1}}\\\cline{1-2}
                \lr{\overline{1}}\\\cline{1-1}
                \end{array}$}
                } \otimes {\def\lr#1{\multicolumn{1}{|@{\hspace{.6ex}}c@{\hspace{.6ex}}|}{\raisebox{-.3ex}{$#1$}}}
                \raisebox{-.6ex}{$\begin{array}[b]{*{1}c}\cline{1-1}
                \lr{2}\\\cline{1-1}
                \end{array}$}
                }
            """
            from sage.misc.latex import latex
            return r" \otimes ".join([latex(self.value[0]),
                                      latex_dual(self.value[1]),
                                      latex(self.value[2])])

        def e(self, i):
            r"""
            Return the action of the crystal operator `e_i` on ``self``.

            EXAMPLES::

                sage: K = crystals.KacModule(['A', [2,2]], [2,1], [1])
                sage: mg = K.module_generator()
                sage: mg.e(0)
                sage: mg.e(1)
                sage: mg.e(-1)
                sage: b = mg.f_string([1,0,1,-1,-2,0,1,2,0,-2,-1,-1,-1]); b
                ({-e[-3]+e[2], -e[-2]+e[1], -e[-2]+e[2]}, [[-3, -1], [-2]], [[3]])
                sage: b.e(-2)
                sage: b.e(-1)
                ({-e[-3]+e[2], -e[-2]+e[1], -e[-2]+e[2]}, [[-3, -2], [-2]], [[3]])
                sage: b.e(0)
                sage: b.e(1)
                ({-e[-3]+e[1], -e[-2]+e[1], -e[-2]+e[2]}, [[-3, -1], [-2]], [[3]])
                sage: b.e(2)
                ({-e[-3]+e[2], -e[-2]+e[1], -e[-2]+e[2]}, [[-3, -1], [-2]], [[2]])
            """
            if i == 0:
                x = self.value[0].e(i)
                if x is None:
                    return None
                return type(self)(self.parent(), (x, self.value[1], self.value[2]))
            if i > 0:
                if self.value[0].epsilon(i) > self.value[2].phi(i):
                    x = self.value[0].e(i)
                    if x is None:
                        return None
                    return type(self)(self.parent(), (x, self.value[1], self.value[2]))
                else:
                    x = self.value[2].e(i)
                    if x is None:
                        return None
                    return type(self)(self.parent(), (self.value[0], self.value[1], x))
            # else i < 0
            M = self.parent()._cartan_type.m + 1
            if self.value[0].phi(i) < self.value[1].epsilon(M+i):
                x = self.value[1].e(M+i)
                if x is None:
                    return None
                return type(self)(self.parent(), (self.value[0], x, self.value[2]))
            else:
                x = self.value[0].e(i)
                if x is None:
                    return None
                return type(self)(self.parent(), (x, self.value[1], self.value[2]))

        def f(self, i):
            r"""
            Return the action of the crystal operator `f_i` on ``self``.

            EXAMPLES::

                sage: K = crystals.KacModule(['A', [2,2]], [2,1], [1])
                sage: mg = K.module_generator()
                sage: mg.f(-2)
                ({}, [[-3, -2], [-2]], [[1]])
                sage: mg.f(-1)
                ({}, [[-3, -3], [-1]], [[1]])
                sage: mg.f(0)
                ({-e[-1]+e[1]}, [[-3, -3], [-2]], [[1]])
                sage: mg.f(1)
                ({}, [[-3, -3], [-2]], [[2]])
                sage: mg.f(2)
                sage: b = mg.f_string([1,0,1,-1,-2,0,1,2,0,-2,-1,2,0]); b
                ({-e[-3]+e[3], -e[-2]+e[1], -e[-1]+e[1], -e[-1]+e[2]},
                 [[-3, -2], [-2]], [[3]])
            """
            if i == 0:
                x = self.value[0].f(i)
                if x is None:
                    return None
                return type(self)(self.parent(), (x, self.value[1], self.value[2]))
            if i > 0:
                if self.value[0].epsilon(i) < self.value[2].phi(i):
                    x = self.value[2].f(i)
                    if x is None:
                        return None
                    return type(self)(self.parent(), (self.value[0], self.value[1], x))
                else:
                    x = self.value[0].f(i)
                    if x is None:
                        return None
                    return type(self)(self.parent(), (x, self.value[1], self.value[2]))
            # else i < 0
            M = self.parent()._cartan_type.m + 1
            if self.value[0].phi(i) > self.value[1].epsilon(M+i):
                x = self.value[0].f(i)
                if x is None:
                    return None
                return type(self)(self.parent(), (x, self.value[1], self.value[2]))
            else:
                x = self.value[1].f(M+i)
                if x is None:
                    return None
                return type(self)(self.parent(), (self.value[0], x, self.value[2]))

        def weight(self):
            r"""
            Return weight of ``self``.

            EXAMPLES::

                sage: K = crystals.KacModule(['A', [3,2]], [2,1], [5,1])
                sage: mg = K.module_generator()
                sage: mg.weight()
                (2, 1, 0, 0, 5, 1, 0)
                sage: mg.weight().is_dominant()
                True
                sage: mg.f(0).weight()
                (2, 1, 0, -1, 6, 1, 0)
                sage: b = mg.f_string([2,1,-3,-2,-1,1,1,0,-2,-1,2,1,1,1,0,2,-3,-2,-1])
                sage: b.weight()
                (0, 0, 0, 1, 1, 4, 3)
            """
            e = self.parent().weight_lattice_realization().basis()
            M = self.parent()._cartan_type.m + 1
            wt = self.value[0].weight()
            wt += sum(c*e[i-M] for i,c in self.value[1].weight())
            wt += sum(c*e[i+1] for i,c in self.value[2].weight())
            return wt

#####################################################################
## Helper functions


def to_dual_tableau(elt):
    r"""
    Return a type `A_n` crystal tableau ``elt`` as a tableau expressed
    in terms of dual letters.

    The dual letter of `k` is expressed as `\overline{n+2-k}` represented
    as `-(n+2-k)`.

    EXAMPLES::

        sage: from sage.combinat.crystals.kac_modules import to_dual_tableau
        sage: T = crystals.Tableaux(['A',2], shape=[2,1])
        sage: ascii_art([to_dual_tableau(t) for t in T])
        [  -3 -3   -3 -2   -3 -1   -3 -1   -2 -1   -3 -3   -3 -2   -2 -2 ]
        [  -2   ,  -2   ,  -2   ,  -1   ,  -1   ,  -1   ,  -1   ,  -1    ]

    TESTS:

    Check that :issue:`23935` is fixed::

        sage: from sage.combinat.crystals.kac_modules import to_dual_tableau
        sage: T = crystals.Tableaux(['A',2], shape=[])
        sage: to_dual_tableau(T[0])
        []

        sage: Ktriv = crystals.KacModule(['A',[1,1]], [], [])
        sage: Ktriv.module_generator()
        ({}, [], [])
    """
    from sage.combinat.tableau import Tableau
    M = elt.parent().cartan_type().rank() + 2
    if not elt:
        return Tableau([])
    tab = [ [elt[0].value-M] ]
    for i in range(1, len(elt)):
        if elt[i-1] < elt[i] or (elt[i-1].value != 0 and elt[i-1] == elt[i]):
            tab.append([elt[i].value-M])
        else:
            tab[len(tab)-1].append(elt[i].value-M)
    for x in tab:
        x.reverse()
    return Tableau(tab).conjugate()


def latex_dual(elt):
    r"""
    Return a latex representation of a type `A_n` crystal tableau ``elt``
    expressed in terms of dual letters.

    The dual letter of `k` is expressed as `\overline{n+2-k}`.

    EXAMPLES::

        sage: from sage.combinat.crystals.kac_modules import latex_dual
        sage: T = crystals.Tableaux(['A',2], shape=[2,1])
        sage: print(latex_dual(T[0]))
        {\def\lr#1{\multicolumn{1}{|@{\hspace{.6ex}}c@{\hspace{.6ex}}|}{\raisebox{-.3ex}{$#1$}}}
        \raisebox{-.6ex}{$\begin{array}[b]{*{2}c}\cline{1-2}
        \lr{\overline{3}}&\lr{\overline{3}}\\\cline{1-2}
        \lr{\overline{2}}\\\cline{1-1}
        \end{array}$}
        }
    """
    M = elt.parent().cartan_type().rank() + 2
    from sage.combinat.tableau import Tableau
    from sage.combinat.output import tex_from_array
    # Modified version of to_tableau() to have the entries be letters
    #   rather than their values
    if not elt:
        return "{\\emptyset}"

    tab = [ ["\\overline{{{}}}".format(M-elt[0].value)] ]
    for i in range(1, len(elt)):
        if elt[i-1] < elt[i] or (elt[i-1].value != 0 and elt[i-1] == elt[i]):
            tab.append(["\\overline{{{}}}".format(M-elt[i].value)])
        else:
            l = len(tab)-1
            tab[l].append("\\overline{{{}}}".format(M-elt[i].value))
    for x in tab:
        x.reverse()

    T = Tableau(tab).conjugate()
    return tex_from_array([list(row) for row in T])
