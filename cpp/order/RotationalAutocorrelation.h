// Copyright (c) 2010-2019 The Regents of the University of Michigan
// This file is from the freud project, released under the BSD 3-Clause License.

#ifndef ROTATIONAL_AUTOCORRELATION_H
#define ROTATIONAL_AUTOCORRELATION_H

#include <cassert>
#include <complex>
#include <memory>
#include <tbb/tbb.h>

#include "VectorMath.h"

/*! \file RotationalAutocorrelation.h
    \brief Defines the RotationalAutocorrelation class, which computes the total
    rotational autocorrelation for a system's orientations against its initial
    orientations.
*/

namespace freud { namespace order {

//! Convert a quaternion to complex coordinates.
/*! \param q The quaternion to generate complex coordinates for.
 *  \return A pair containing the coordinates (xi, zeta).
 *
 *  The set of quaternions are isomorphic to the special unitary group of
 *  degree 2 SU(2), which forms a double cover of the 3D rotation group SO(3).
 *  SU(2) is also diffeomorphic to the 3-sphere S3 (see
 *  https://en.wikipedia.org/wiki/Special_unitary_group#Diffeomorphism_with_S3,
 *  for example), meaning that we can represent quaternions in terms of two
 *  complex numbers that map out hyperspherical coordinates in 3 dimensions.
 *  This function generates that mapping.
 */
std::pair<std::complex<float>, std::complex<float>> quat_to_greek(const quat<float>& q);

//! Compute the total rotational autocorrelation for a set of orientations.
/*! The desired autocorrelation function is the rotational analog of the
 *  dynamic structure factor, which provides information on the dynamics of
 *  systems of points. Calculating this quantity requires a generalization of
 *  the Fourier transform to a different domain, namely the rotation group
 *  SO(3). This computation can be performed using a hyperspherical coordinate
 *  representation of the rotations. For details, see "Design rules for
 *  engineering colloidal plastic crystals of hard polyhedra – phase behavior
 *  and directional entropic forces" by Karas et al. (currently in preparation).
 */
class RotationalAutocorrelation
{
public:
    //! Explicit default constructor for Cython.
    RotationalAutocorrelation() {}

    //! Constructor
    /*! \param l The order of the spherical harmonic.
     */
    RotationalAutocorrelation(unsigned int l) : m_l(l), m_N(0), m_Ft(0)
    {
        // For efficiency, precompute all required factorials;
        m_factorials = std::shared_ptr<unsigned int>(new unsigned int[m_l+1], std::default_delete<unsigned int[]>());
        memset((void*) m_factorials.get(), 0, sizeof(unsigned int) * (m_l+1));
        m_factorials.get()[0] = 1;
        for (unsigned int i = 1; i <= m_l; i++)
        {
            m_factorials.get()[i] = i*m_factorials.get()[i-1];
        }
    }

    //! Destructor
    ~RotationalAutocorrelation() {}

    //! Get the quantum number l used in calculations.
    unsigned int getL()
    {
        return m_l;
    }

    //! Get the number of orientations used in the last call to compute.
    unsigned int getN()
    {
        return m_N;
    }

    //! Get a reference to the last computed rotational autocorrelation array.
    std::shared_ptr<std::complex<float>> getRAArray()
    {
        return m_RA_array;
    }

    //! Get a reference to the last computed value of the rotational autocorrelation.
    float getRotationalAutocorrelation()
    {
        return m_Ft;
    }

    //! Compute the rotational autocorrelation.
    /*! \param ref_ors Quaternions in initial frame.
     *  \param ors Quaternions in current frame.
     *  \param N The number of orientations.
     *
     *  This function loops over all provided orientations and reference
     *  orientations and computes their hyperspherical harmonics for the
     *  desired range of quantum numbers. For each orientation/reference
     *  pair, the autocorrelation value is computed as the inner product of
     *  these two hyperspherical harmonics. The value of the autocorrelation
     *  for the whole system is then the average of the real parts of the
     *  autocorrelation for the whole system.
     */
    void compute(const quat<float>* ref_ors, const quat<float>* ors, unsigned int N);

private:
    //! Compute a hyperspherical harmonic.
    /*! \param xi The first complex number coordinate.
     *  \param zeta The second complex number coordinate.
     *  \param l The azimuthal quantum number.
     *  \param m1 The first magnetic quantum number.
     *  \param m2 The second magnetic quantum number.
     *  \return The value of the hyperspherical harmonic (l, m1, m2) at (xi, zeta).
     *
     *  The hyperspherical harmonic function is a generalization of spherical
     *  harmonics from the 2-sphere to the 3-sphere. For details, see Harmonic
     *  functions and matrix elements for hyperspherical quantum field models
     *  (https://doi.org/10.1063/1.526210). The function needs to be a class
     *  method to access the cached factorial values for the class's value of
     *  m_l.
     */
    std::complex<float> hypersphere_harmonic(const std::complex<float> xi, std::complex<float> zeta, const unsigned int l,
                                             const unsigned int m1, const unsigned int m2);

    unsigned int m_l;          //!< Order of the hyperspherical harmonic.
    unsigned int m_N; //!< Last number of orientations used in compute.
    float m_Ft;       //!< Real value of calculated RA function.

    std::shared_ptr<std::complex<float>> m_RA_array; //!< Array of RA values per particle
    std::shared_ptr<unsigned int> m_factorials; //!< Array of cached factorials
};

}; }; // end namespace freud::order

#endif // ROTATIONAL_AUTOCORRELATION_H
