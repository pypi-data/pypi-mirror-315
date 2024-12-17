from math import ceil
from typing import Literal, Optional, Tuple

import exo_k as xk
import numba
import numpy as np
from exo_k import Spectrum
from tqdm.auto import tqdm

from pytmosph3r.log import Logger
from pytmosph3r.util.geometry import cos_central_angle

from ..aerosols import PrepareAerosols
from ..atmosphere import Atmosphere


@numba.njit(cache=True)
def surface_projection(local_latitudes, n_per_latitudes: int,
                       local_longitudes, n_per_longitudes: int, n_total_longitudes: int,
                       obs_latitude: float, obs_longitude: float,
                       planet_radius: float,
                       star_pos: Optional[Tuple[float, float]]) -> Tuple[float, float, float, float]:
    """Compute surface projection of :attr:`local_latitudes` and :attr:`local_longitudes` on the plane of
    the sky (as seen from the observer). :attr:`local_projection` is the output of the function. """

    visible_projected_surface: float = 0.
    effective_flux_attenuation_factor: float = 0.

    effective_mu_star: float = 0.
    effective_mu_obs: float = 0.

    for i in range(n_per_latitudes):
        lat_bounds: np.ndarray = np.array([local_latitudes[i], local_latitudes[i + 1]])
        latitude: np.ndarray = np.mean(lat_bounds)
        surface: float = (2 * np.pi * planet_radius ** 2
                          * (np.sin(lat_bounds[1]) - np.sin(lat_bounds[0])) / n_total_longitudes)

        for j in range(n_per_longitudes):
            long_bounds = np.array([local_longitudes[j], local_longitudes[j + 1]])
            longitude = np.mean(long_bounds)

            # phi = central angle between (lat, lon) and observer (@ infinite distance)
            mu_obs = cos_central_angle(latitude, longitude, obs_latitude, obs_longitude)

            if mu_obs <= 0:
                # Surface not seen, skip.
                continue

            # Take into account the visible surface.
            visible_projected_surface += mu_obs * surface
            effective_mu_obs += mu_obs * mu_obs * surface

            # Now, compute mu_star and take into account its effect, if required.
            if star_pos is not None:
                mu_star = cos_central_angle(latitude, longitude, star_pos[0], star_pos[1])

                # The star does not illuminate the surface.
                if mu_star <= 0:
                    continue

                effective_flux_attenuation_factor += mu_obs * surface * mu_star
                # JL2024 we weigh the flux received by the surface by both the stellar and observer angles.
                # We will then normalize by the total visible projected surface afterward.
                # This seems exact for a lambertian reflector.
                effective_mu_star += mu_obs * surface * mu_star * mu_star

    if visible_projected_surface > 0.:
        effective_mu_obs /= visible_projected_surface

        effective_mu_star /= visible_projected_surface
        effective_flux_attenuation_factor /= visible_projected_surface

    return visible_projected_surface, effective_mu_obs, effective_flux_attenuation_factor, effective_mu_star


class Emission(Logger):
    """The emission module computes the flux emitted by a body by iterating over the latitudes and longitudes of the model. It relies on `Exo_k <http://perso.astrophy.u-bordeaux.fr/~jleconte/exo_k-doc/autoapi/exo_k/atm/index.html?highlight=emission#exo_k.atm.Atm.emission_spectrum_2stream>`_ for the computation of the 1D flux in each column.
    The flux is then scaled with respected to the surface of the atmosphere projected onto the plane of the sky.
    All options are deactivated by default.

    Args:
        planet_to_star_flux_ratio (bool): The output spectrum will be a ratio between the flux of the planet and that of the star (instead of the flux of the planet).

        surface_resolution (int) : Number of grid points to calculate the projected surface (the more points, the more accurate). Defaults to 500.

        store_raw_flux (bool) : Whether to store raw flux (over each (latitude, longitude)).

        top_flux_from_star (bool) : Whether to use the star flux as top flux (weighted by the cosines of the angle between the column (lat,lon) and the star).

        mu_from_obs (bool) : Whether to use the position of the observer for computing a :math:`\\mu_0` for :func:`emission_spectrum_2stream`.

        compute_contribution_function (bool) : Compute the contribution function. See `documentation of Exo_k <http://perso.astrophy.u-bordeaux.fr/~jleconte/exo_k-doc/autoapi/exo_k/atm/index.html#exo_k.atm.Atm.contribution_function>`

        stellar_mode: Set the method to be used to take into account the star flux. See `documentation of Exo_k <http://perso.astrophy.u-bordeaux.fr/~jleconte/exo_k-doc/autoapi/exo_k/atm/index.html#exo_k.atm.Atm.emission_spectrum_2stream>`

        kwargs (dict): See `documentation of Exo_k <http://perso.astrophy.u-bordeaux.fr/~jleconte/exo_k-doc/autoapi/exo_k/atm/index.html?highlight=emission#exo_k.atm.Atm.emission_spectrum_2stream>`_ to see what other options are available.

    Returns: (Spectrum): If :attr:`planet_to_star_flux_ratio` is True, the planet-to-star flux ratio
    (:math:`F_P/F_S * (R_P/R_S)^2`), else the planet flux (in :math:`W/m^2/cm^{-1}`).
    """

    def __init__(self, planet_to_star_flux_ratio: bool = False,
                 planet_to_top_flux_ratio: bool = False,
                 surface_resolution: int = 500,
                 store_raw_flux: bool = False,
                 top_flux_from_star: bool = False,
                 mu_from_obs: bool = False,
                 compute_contribution_function: bool = False,
                 stellar_mode: Literal['diffusive', 'collimated'] = 'diffusive',
                 **kwargs):
        super().__init__(self.__class__.__name__)

        if top_flux_from_star is False and planet_to_star_flux_ratio is True:
            raise ValueError('`top_flux_from_star` need to be enabled to use `planet_to_star_flux_ratio`.')
        if planet_to_top_flux_ratio is True and planet_to_star_flux_ratio is True:
            raise ValueError('Chooseonly one ratio!')

        self.planet_to_star_flux_ratio: bool = planet_to_star_flux_ratio
        """Returns the planet to star flux ratio instead of the planet flux."""

        self.planet_to_top_flux_ratio = planet_to_top_flux_ratio
        """Returns the planet to top flux ratio instead of the planet flux."""

        self.surface_resolution: Optional[int] = surface_resolution
        """Number of grid points to calculate projected surface."""

        self.store_raw_flux: bool = store_raw_flux
        """Whether or not to store raw flux (over each (latitude, longitude))."""

        self.top_flux_from_star: bool = top_flux_from_star
        """Whether or not to use the star flux as top flux (weighted by the cosine of the angle between the
        column (lat,lon) and the star). """

        self.mu_from_obs: bool = mu_from_obs
        r"""Use the position of the observer for computing a :math:`\mu_0` for
        :func:`emission_spectrum_2stream`. """

        self.compute_contribution_function: bool = compute_contribution_function
        """Allow to compute the contribution function."""

        self.stellar_mode: Literal['diffusive', 'collimated'] = stellar_mode
        """Method to take into account the top flux from star (if `self.top_flux_from_star` is `True`)"""

        self.kwargs = kwargs

        self.spectrum: Optional[Spectrum] = None
        """Output spectrum (Exo_k object)."""

        self.spectrum_normalized: Optional[Spectrum] = None
        """Output spectrum (Exo_k object) normalized with the stellar flux."""

        self.factor_normalized : Optional[Spectrum] = None

        # Attribute created by the methods
        # self.model: Optional['Model'] = None
        # self.observer: Optional['Observer'] = None
        # self.projected_surface: Optional[np.ndarray] = None
        # self.spectrum: Spectrum
        # self.raw_flux: Optional[np.ndarray] = None
        # self.observer_longitudes: Optional[float] = None
        # self.phase_curve_flux: Optional[np.ndarray] = None

    def build(self, model):
        """No need for an altitude-based grid (as done in transmission), so we just copy the input grid.
        """
        self.model = model

        if hasattr(model, "emission_atmosphere") and model.emission_atmosphere is not None:
            self.atmosphere = model.emission_atmosphere  # simple ref
        else:
            self.atmosphere = model.input_atmosphere  # simple ref

        self.atmosphere.build(model)
        self.observer = model.observer

    def compute_projection(self, star_pos: Optional[Tuple[float, float]]):
        """Compute the projection surface of the grid cells over the plane of the sky."""
        obs = self.model.observer
        atm = self.atmosphere

        self.visible_projected_surface = np.zeros(atm.shape[1:])
        self.effective_mu_obs = np.ones(atm.shape[1:]) * 0.5

        self.effective_flux_attenuation_factor = np.zeros(atm.shape[1:])
        self.effective_mu_star = np.ones(atm.shape[1:]) * 0.5

        latitudes = atm.grid.latitudes
        longitudes = atm.grid.all_longitudes

        n_per_longitudes = int(ceil(self.surface_resolution / atm.grid.n_longitudes))
        n_total_longitudes = n_per_longitudes * atm.grid.n_longitudes
        n_per_latitudes = int(ceil(self.surface_resolution / atm.grid.n_latitudes))
        n_total_latitudes = n_per_latitudes * max(atm.grid.n_latitudes - 2, 1)

        # discretize surface among n_total_{latitudes, longitudes} (for better accuracy)
        surface_longitudes = np.linspace(longitudes[0], longitudes[-1], n_total_longitudes + 1)
        surface_latitudes = np.linspace(latitudes[1], latitudes[-2],
                                        n_total_latitudes + 1)  # except poles, since they're halved

        for lat, lon in atm.grid.walk([1, 2]):
            # Create local subdivisions of latitude and longitude to compute surface projection with a better accuracy.
            if lat == 0 or lat == atm.n_latitudes - 1:
                # exception for the poles, because they're halved
                local_latitudes = np.linspace(latitudes[lat], latitudes[lat + 1], n_per_latitudes + 1)
            else:
                local_latitudes = surface_latitudes[(lat - 1) * n_per_latitudes:lat * n_per_latitudes + 1]
                assert np.isclose(local_latitudes[-1], latitudes[lat + 1]), \
                    f'Local latitude ({local_latitudes[-1]}) is not correct ({latitudes[lat + 1]}). Report this as a bug.'
                assert np.isclose(local_latitudes[0], latitudes[lat]), \
                    "Local latitude is not correct. Report this as a bug."

            local_longitudes = surface_longitudes[lon * n_per_longitudes:(lon + 1) * n_per_longitudes + 1]

            self.visible_projected_surface[lat, lon], self.effective_mu_obs[lat, lon], \
                self.effective_flux_attenuation_factor[lat, lon], self.effective_mu_star[lat, lon] = \
                surface_projection(local_latitudes, n_per_latitudes,
                                   local_longitudes, n_per_longitudes, n_total_longitudes,
                                   obs.latitude, obs.longitude,
                                   self.model.planet.radius,
                                   star_pos=star_pos)


    def compute(self, model):
        """Iterate over vertical columns (lat/lon) of the model, in which we use the exo_k 1D two-stream emission function (emission_spectrum_2stream() for the `Atm` class). Then integrate the output flux in the direction of the observer.
        For that, we compute the solid angle associated with the position of the observer, projecting the visible surface of the atmosphere onto the plane of the sky.
        The flux is scaled with respect to that projected surface.
        If :attr:`planet_to_star_flux_ratio` is True, the flux is scaled to the flux of the star (a blackbody) and
        stored in `self.spectrum_normalized`.
        If the phase curve mode is activated, this function also computes a :attr:`phase_curve` object with the spectrum associated to all :attr:`n_phases` phase/observer longitudes (see :func:`compute_phase_curve`).

        Args:
            model (:class:`~pytmosph3r.model.model.Model`): Model in which to read latitudes, longitudes, pressure, etc.

        Returns:
            Spectrum (exo_k object): Spectrum, planet flux (stored in `self.spectrum`). `Self.spectrum_normalized`
            stores the planet-to-star ratio if `self.planet_to_star_flux_ratio` is `True`.
        """
        if "dummy" in self.kwargs:
            return
        if model.parallel:
            model = model.parallel.synchronize(model) # get model from P0

        self.model = model
        atm: Atmosphere = self.atmosphere
        opacity = self.model.opacity

        self.info("Computing output flux...")
        self.spectrum: Spectrum = xk.Spectrum(0, opacity.k_data.wns, opacity.k_data.wnedges)

        # To allow comparison, divide the flux by the planet surface i.e., add [/m^2]
        self.factor = np.pi * self.model.planet.radius ** 2

        star_spectrum_top_atm: Optional[Spectrum] = None  # stellar spectrum at the top of the planet.
        star_flux_top_atm: Optional[float] = None  # total stellar flux at the top of the planet.
        star_pos: Optional[Tuple[float, float]] = None # Position of the star on from the pov of the planet.

        if self.store_raw_flux is True:
            self.raw_flux = np.zeros((atm.n_latitudes, atm.n_longitudes, model.opacity.k_data.Nw))  # F TOA (W/m2/cm-1)
            self.raw_flux_toa = np.zeros((atm.n_latitudes, atm.n_longitudes))  # Flux TOA (W/m2)

        if self.planet_to_star_flux_ratio is True:
            # Normalize with star flux, the star_flux_surface is taken at the surface of the star
            star_flux_surface = self.model.star.spectrum_like(opacity)

            # We cancel the [/m^2] while also computing the total flux from the star
            # (pi is already taken into account in the star_flux, see BB)
            self.factor_normalized: xk.Spectrum = star_flux_surface * self.factor * (
                    self.model.star.radius / self.model.planet.radius) ** 2

        if self.top_flux_from_star is True:
            if self.model.orbit is None:
                raise ValueError("Can't know star position without an orbit.")

            star_pos = self.model.orbit.star_coordinates

            if star_pos is None:
                raise ValueError("Define star coordinates to proceed with the option 'top_flux_from_star'.")

            # We compute the stellar spectrum and total flux at the planet
            star_spectrum_top_atm: xk.Spectrum = model.star.spectrum_like(spectrum=opacity,
                                                                          distance=model.orbit.r())
            star_flux_top_atm: float = star_spectrum_top_atm.total

            if self.planet_to_top_flux_ratio is True:
                self.factor_normalized: xk.Spectrum = star_spectrum_top_atm * self.factor

        if self.compute_contribution_function is True:
            self.contribution_function: np.ndarray = np.zeros((atm.n_latitudes, atm.n_longitudes, atm.grid.n_vertical - 1,))

        longitudes = atm.grid.mid_longitudes
        if atm.n_latitudes < 2 and atm.n_longitudes > 1:
            longitudes = tqdm(atm.grid.mid_longitudes, leave=None)

        # Compute the projection with `star_pos` set if we require stellar illumination computing.
        self.compute_projection(star_pos)

        for lat, latitude in enumerate(tqdm(atm.grid.mid_latitudes, leave=False, )):
            for lon, longitude in enumerate(longitudes):
                if self.mu_from_obs is True:
                    if self.effective_mu_obs[lat, lon] <= 0.:
                        # Surface is not seen by the observer
                        continue

                    self.kwargs["mu0"] = self.effective_mu_obs[lat, lon]

                if not self.store_raw_flux is True:
                    # Apply skip check if we don't want the raw flux for each column of the atmosphere.
                    if self.visible_projected_surface[lat, lon] <= 0:
                        # Surface is not seen by the observer
                        continue

                # The data should go from the top to the bottom in Exo_k (+ pressure in log10)
                layers = slice(None, None,-1)
                coordinates = (layers, lat, lon)

                mu_star: Optional[float] = None
                flux_top_dw: Optional[float] = None
                albedo_params = {}

                # Compute the diffusive flux at the top coming from the star.
                if self.top_flux_from_star is True:
                    # Flux received from the star, need to be positive else `None` to not be taken into account
                    mu_star = self.effective_mu_star[lat, lon]
                    flux_top_dw = star_flux_top_atm * self.effective_flux_attenuation_factor[lat, lon]  \
                        if self.effective_flux_attenuation_factor[lat, lon] > 0. else None

                    # In diffusive mode or when there is no flux, the angle is unnecessary.
                    # A negative mu_star implies a null flux_top_dw, so this case is also caught here
                    mu_star = None if self.stellar_mode == 'diffusive' or flux_top_dw is None else mu_star

                # Set value for both cases ie also when not treating stellar flux
                stellar_mode = self.stellar_mode if mu_star is not None else 'diffusive'
                flux_top_dw: float = flux_top_dw if flux_top_dw is not None else 0.

                # Prepare albedo parameters
                if atm.albedo_surf is not None:
                    albedo_params['albedo_surf'] = atm.albedo_surf[(lat, lon)]
                if atm.wn_albedo_cutoff is not None:
                    albedo_params['wn_albedo_cutoff'] = atm.wn_albedo_cutoff[(lat, lon)]

                # Select data at coordinates lat x lon
                logplay = np.log10(atm.pressure[coordinates])
                tlay = atm.temperature[coordinates]
                gas_vmr = {}

                for gas, vmr in atm.gas_mix_ratio.items():
                    if isinstance(vmr, (str, int, float)):
                        gas_vmr[gas] = vmr
                    else:
                        gas_vmr[gas] = vmr[coordinates]

                prepare_aerosols = PrepareAerosols(self.model, atm, atm.n_vertical)
                aer_reff_densities = prepare_aerosols.compute(slice(None, None), coordinates)

                # Effectively compute the flux via the 2stream function from exo_k
                xk_atm = xk.Atm(logplay=logplay, tlay=tlay, grav=self.model.planet.surface_gravity,
                                composition=gas_vmr, aerosols=aer_reff_densities,
                                k_database=opacity.k_data, cia_database=opacity.cia_data,
                                a_database=opacity.aerosol_data, Rp=model.planet.radius, rcp=atm.rcp,
                                **albedo_params)


                flux: xk.Spectrum = xk_atm.emission_spectrum_2stream(rayleigh=opacity.rayleigh,
                                                                     log_interp=False,
                                                                     flux_top_dw=flux_top_dw,
                                                                     stellar_mode=stellar_mode,
                                                                     mu_star=mu_star,
                                                                     stellar_spectrum=star_spectrum_top_atm,
                                                                     **self.kwargs)

                if self.compute_contribution_function:
                    # Compute contribution (Shape: (Nlay - 1, Nw)) and perform the spectral integration.
                    # Should return an array of the shape (Nlay - 1,)

                    # TODO: Replace manual integration by `xk_atm.spectral_integration` but without the
                    #   `g_integration`.
                    self.contribution_function[lat, lon, :] = np.sum(xk_atm.contribution_function() * xk_atm.dwnedges, axis=-1)

                if self.store_raw_flux:
                    self.raw_flux[lat, lon] = flux.value  # * self.model.surface[lat, lon] / (np.pi*self.model.planet.radius ** 2)
                    self.raw_flux_toa[lat, lon] = flux.total

                if self.visible_projected_surface[lat, lon] >= 0.:
                    flux *= self.visible_projected_surface[lat, lon]
                    self.spectrum += flux

        if self.compute_contribution_function:
            # Normalize contributions across all columns.
            self.contribution_function /= self.contribution_function.max()

        self.info("DONE")

        if self.planet_to_star_flux_ratio is True or self.planet_to_top_flux_ratio is True:
            self.spectrum_normalized = self.spectrum.copy()
            self.spectrum_normalized /= self.factor_normalized

        self.spectrum /= self.factor

        return self.spectrum

    def outputs(self):
        outputs = ["spectrum", "spectrum_normalized", "raw_flux", "visible_projected_surface"]
        if self.compute_contribution_function:
            outputs += ['contribution_function']


        return outputs
