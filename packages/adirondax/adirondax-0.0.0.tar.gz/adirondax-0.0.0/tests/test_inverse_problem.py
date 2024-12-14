import os
import jax
import jax.numpy as jnp
import adirondax as adx
from jaxopt import ScipyMinimize
import matplotlib.image as img


def read_target():
    file_path = os.path.join(os.path.dirname(__file__), "../examples/schrodinger_poisson/target.png")
    target_data = img.imread(file_path)[:, :, 0]
    rho_target = jnp.flipud(jnp.array(target_data, dtype=float))
    rho_target = 1.0 - 0.5 * (rho_target - 0.5)
    rho_target /= jnp.mean(rho_target)
    return rho_target


def set_up_params():
    n = 128
    nt = 100
    t_stop = 0.03
    dt = t_stop / nt
    params = {
        "n": n,
        "t_stop": t_stop,
        "dt": dt,
        "nt": nt,
    }
    return params


def run_forward_model():
    params = set_up_params()
    sim = adx.Simulation(params)
    xlin = jnp.linspace(0.0, 1.0, params["n"])
    x, y = jnp.meshgrid(xlin, xlin, indexing="ij")
    theta = -jnp.exp(-((x - 0.5) ** 2 + (y - 0.5) ** 2))
    psi = jnp.exp(1.0j * theta)
    psi = sim.evolve(psi, params["dt"], params["nt"])
    theta = jnp.angle(psi)
    return jnp.mean(theta)


def solve_inverse_problem():

    rho_target = read_target()
    assert rho_target.shape[0] == 128

    params = set_up_params()

    sim = adx.Simulation(params)

    @jax.jit
    def loss_function(theta, rho_target):
        psi = jnp.exp(1.0j * theta)
        psi = sim.evolve(psi, params["dt"], params["nt"])
        rho = jnp.abs(psi) ** 2
        return jnp.mean((rho - rho_target) ** 2)

    opt = ScipyMinimize(method="l-bfgs-b", fun=loss_function, tol=1e-5)
    theta = jnp.zeros_like(rho_target)
    sol = opt.run(theta, rho_target)
    theta = jnp.mod(sol.params, 2.0 * jnp.pi) - jnp.pi

    return jnp.mean(theta)


def test_forward_model():
    assert abs(run_forward_model() - -0.249652) < 1e-3


def test_solve_inverse_problem():
    assert abs(solve_inverse_problem() - 0.019558249) < 1e-2
