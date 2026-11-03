"""Métricas de validación. Error con signo e_i = y_hat_i - y_i; conservan las unidades de y."""
import numpy as np

def errores(y_est, y_obs):
    return np.asarray(y_est, float) - np.asarray(y_obs, float)

def mae(e):   return float(np.mean(np.abs(e)))
def rmse(e):  return float(np.sqrt(np.mean(np.square(e))))
def emax(e):  return float(np.max(np.abs(e)))

def resumen(y_est, y_obs, unidad=""):
    """Devuelve MAE, RMSE y E_max (misma unidad que la variable) y m."""
    e = errores(y_est, y_obs)
    return {"m": int(e.size), "MAE": mae(e), "RMSE": rmse(e), "E_max": emax(e), "unidad": unidad}
