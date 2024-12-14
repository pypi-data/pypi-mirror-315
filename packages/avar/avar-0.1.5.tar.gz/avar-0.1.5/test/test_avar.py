import numpy as np
import avar

np.random.seed(0)


def test_standard_five():
    # Build time.
    T = 0.01
    t_dur = 200.0
    t = np.arange(0, t_dur, T)
    K = len(t)

    # Constants
    J = 50
    p = avar.params(vc=np.array([0.5, 1.0, 5, 0.5, 0.1]) * 1e-9)

    # Get mean Allan variance from Monte-Carlo noise.
    M = avar.windows(K)
    tau = M*T
    va_real = np.zeros(len(M))
    for j in range(J):
        y = avar.noise(K, T, p)
        va_real += avar.variance(y, M)/J

    # Get the ideal and fitted Allan variances.
    va_ideal, _ = avar.ideal(tau, p)
    va_fit, p_fit = avar.fit(tau, va_ideal, tol=0.001)

    # Verify the component variances are correct.
    er_vc = np.abs(p.vc - p_fit.vc)/p.vc
    assert(np.all(er_vc < 1e-3))

    # Verify the real is close to ideal.
    er_real = np.abs(np.log10(va_ideal) - np.log10(va_real))
    assert(np.all(er_real < 0.1))

    # Verify the fit is close to ideal.
    er_fit = np.abs(np.log10(va_ideal) - np.log10(va_fit))
    assert(np.all(er_fit < 0.1))


def test_two_fogms():
    # Build time.
    T = 0.01
    t_dur = 200.0
    t = np.arange(0, t_dur, T)
    K = len(t)

    # Constants
    J = 50
    p = avar.params(
            vfogm=np.array([1e-8, 1e-7]),
            tfogm=np.array([0.1, 10]))

    # Get mean Allan variance from Monte-Carlo noise.
    M = avar.windows(K)
    tau = M*T
    va_real = np.zeros(len(M))
    for j in range(J):
        y = avar.noise(K, T, p)
        va_real += avar.variance(y, M)/J

    # Get the ideal and fitted Allan variances.
    va_ideal, _ = avar.ideal(tau, p)
    va_fit, p_fit = avar.fit(tau, va_ideal, fogms=2)

    # Verify the component variances are correct.
    er_vfogm = np.abs(p.vfogm - p_fit.vfogm)/p.vfogm
    assert(np.all(er_vfogm < 1e-3))

    # Verify the component time constants are correct.
    er_tfogm = np.abs(p.tfogm - p_fit.tfogm)/p.tfogm
    assert(np.all(er_tfogm < 1e-3))

    # Verify the real is close to ideal.
    er_real = np.abs(np.log10(va_ideal) - np.log10(va_real))
    assert(np.all(er_real < 0.1))

    # Verify the fit is close to ideal.
    er_fit = np.abs(np.log10(va_ideal) - np.log10(va_fit))
    assert(np.all(er_fit < 0.1))
