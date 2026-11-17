import pytest

from app_movil import (
    PerfilMovil,
    PerfilPro,
    PuntosInsuficientesError,
    SuscripcionExpiradaError,
)


@pytest.fixture
def perfil():
    return PerfilMovil("ana")


@pytest.fixture
def perfil_pro():
    return PerfilPro("beto", meses_suscripcion=3)

def test_valores_iniciales(perfil):
    assert perfil.username == "ana"
    assert perfil.gemas == 50
    assert perfil.racha_dias == 1
    assert perfil.notificaciones_activas is True


def test_ganar_gemas_suma_al_saldo(perfil):
    assert perfil.ganar_gemas(25) == 75
    assert perfil.gemas == 75


def test_gastar_gemas_resta_del_saldo(perfil):
    assert perfil.gastar_gemas(20) == 30
    assert perfil.gemas == 30


def test_gastar_todo_el_saldo_deja_cero(perfil):
    assert perfil.gastar_gemas(50) == 0


def test_transacciones_consecutivas_son_consistentes(perfil):
    perfil.ganar_gemas(10)
    perfil.gastar_gemas(30)
    assert perfil.gemas == 30


def test_gemas_iniciales_negativas_lanzan_error():
    with pytest.raises(ValueError):
        PerfilMovil("ana", gemas=-1)


def test_gastar_mas_de_lo_disponible_lanza_error(perfil):
    with pytest.raises(PuntosInsuficientesError):
        perfil.gastar_gemas(51)
    assert perfil.gemas == 50  # el saldo no cambia si falla


@pytest.mark.parametrize("cantidad", [0, -5])
def test_gastar_cantidad_no_positiva_lanza_error(perfil, cantidad):
    with pytest.raises(ValueError):
        perfil.gastar_gemas(cantidad)


def test_perfil_pro_con_meses_invalidos_lanza_error():
    with pytest.raises(ValueError):
        PerfilPro("beto", meses_suscripcion=0)


def test_descarga_con_suscripcion_expirada_lanza_error(perfil_pro):
    perfil_pro.meses_suscripcion = 0
    with pytest.raises(SuscripcionExpiradaError):
        perfil_pro.descargar_contenido_offline()
    assert perfil_pro.es_pro is False


@pytest.mark.parametrize(
    "cantidad, esperado",
    [
        (1, 51),       # límite inferior válido
        (10, 60),
        (100, 150),
        (10_000, 10_050),
    ],
)
def test_ganar_gemas_valores_validos(perfil, cantidad, esperado):
    assert perfil.ganar_gemas(cantidad) == esperado


@pytest.mark.parametrize("cantidad", [0, -1, -100])
def test_ganar_gemas_valores_invalidos(perfil, cantidad):
    with pytest.raises(ValueError):
        perfil.ganar_gemas(cantidad)


def test_perfil_pro_hereda_de_perfil_movil(perfil_pro):
    assert isinstance(perfil_pro, PerfilPro)
    assert isinstance(perfil_pro, PerfilMovil)
    assert issubclass(PerfilPro, PerfilMovil)


def test_perfil_base_no_es_perfil_pro(perfil):
    assert not isinstance(perfil, PerfilPro)


def test_perfil_pro_estado_inicial_y_metodos_heredados(perfil_pro):
    assert perfil_pro.es_pro is True
    assert perfil_pro.meses_suscripcion == 3
    assert perfil_pro.gemas == 50
    assert perfil_pro.ganar_gemas(5) == 55


def test_descarga_offline_exitosa(perfil_pro):
    mensaje = perfil_pro.descargar_contenido_offline()
    assert isinstance(mensaje, str)
    assert "correctamente" in mensaje
    assert perfil_pro.es_pro is True


def test_excepciones_del_dominio_son_exception():
    assert issubclass(SuscripcionExpiradaError, Exception)
    assert issubclass(PuntosInsuficientesError, Exception)
