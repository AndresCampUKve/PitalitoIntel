/**
 * ============================================================
 * MOTOR BONANZA — Motor de Inteligencia Financiera en C++
 * Proyecto: Mi APP ✹Bonanza  |  Pitalito, Huila
 * ============================================================
 * 
 * USO:
 *   motor.exe <precio_cafe> <trm> <tasa_banrep>
 *   motor.exe 1850000 4350 9.75
 *
 * SALIDA: JSON con el score de riesgo, clima, tendencia y proyección
 *
 * COMPILAR:
 *   g++ -O2 -o motor motor.cpp -lm
 *   (Windows): g++ -O2 -o motor.exe motor.cpp
 *
 * El script scraper.py llama a este binario y parsea el JSON resultante.
 * ============================================================
 */

#include <iostream>
#include <sstream>
#include <cmath>
#include <cstring>
#include <string>
#include <vector>
#include <algorithm>
#include <ctime>

// ============================================================
// CONSTANTES DEL MODELO FINANCIERO DE PITALITO
// ============================================================

// Rangos históricos reales del mercado cafetero colombiano
const double CAFE_TECHO_BONANZA  = 2000000.0;  // $2M/carga = excelente
const double CAFE_ESTABLE_ALTO   = 1750000.0;  // $1.75M = bueno
const double CAFE_ESTABLE_BAJO   = 1500000.0;  // $1.5M = neutral
const double CAFE_PISO_RIESGO    = 1200000.0;  // <$1.2M = tormenta

// Rangos TRM (COP/USD)
const double TRM_BAJO             = 3900.0;    // Dólar barato = importar es bueno
const double TRM_NEUTRAL_MAX      = 4300.0;    // Zona neutra
const double TRM_ALTO             = 4700.0;    // Dólar caro = costos suben
const double TRM_CRITICO          = 5200.0;    // Zona de emergencia

// Rango BanRep (Tasa de interés base Colombia)
const double BR_BAJO              = 6.0;       // Crédito accesible
const double BR_NEUTRAL           = 9.0;
const double BR_ALTO              = 12.0;
const double BR_CRITICO           = 15.0;

// Pesos del modelo (suman 100%)
const double PESO_CAFE            = 0.50;      // El café es el corazón de Pitalito
const double PESO_TRM             = 0.30;      // El dólar afecta costos de producción
const double PESO_BANREP          = 0.20;      // El crédito impacta liquidez regional

// ============================================================
// ESTRUCTURAS DE DATOS
// ============================================================

struct ResultadoMotor {
    double          score;          // 0-100 (0=sin riesgo, 100=riesgo máximo)
    std::string     clima;          // "Bonanza" | "Estabilidad" | "Tormenta"
    std::string     senal_cafe;     // Señal específica del café
    std::string     senal_trm;     // Señal específica de la TRM
    std::string     senal_br;      // Señal tasa BanRep
    double          score_cafe;     // Componente café (0-100)
    double          score_trm;      // Componente TRM  (0-100)
    double          score_br;       // Componente BanRep (0-100)
    double          proj_7d;        // Proyección score en 7 días
    double          proj_30d;       // Proyección score en 30 días
    std::string     recomendacion;  // Texto de recomendación corta
    int             liquidez_pct;   // Estimado de liquidez regional (0-100%)
};

// ============================================================
// MÓDULO 1 — SCORE DEL CAFÉ (peso: 50%)
// Algoritmo: Función sigmoidal suavizada sobre rangos históricos
// ============================================================

double calcularScoreCafe(double precio) {
    if (precio <= 0) return 80.0;  // dato inválido → riesgo alto

    if (precio >= CAFE_TECHO_BONANZA)           return 5.0;   // Bonanza máxima
    if (precio >= CAFE_ESTABLE_ALTO)  {
        // Interpolación lineal entre 5% y 25%
        double t = (precio - CAFE_ESTABLE_ALTO) / (CAFE_TECHO_BONANZA - CAFE_ESTABLE_ALTO);
        return 25.0 - (t * 20.0);
    }
    if (precio >= CAFE_ESTABLE_BAJO) {
        double t = (precio - CAFE_ESTABLE_BAJO) / (CAFE_ESTABLE_ALTO - CAFE_ESTABLE_BAJO);
        return 50.0 - (t * 25.0);
    }
    if (precio >= CAFE_PISO_RIESGO) {
        double t = (precio - CAFE_PISO_RIESGO) / (CAFE_ESTABLE_BAJO - CAFE_PISO_RIESGO);
        return 80.0 - (t * 30.0);
    }
    // Bajo del piso de riesgo → máximo riesgo
    return 95.0;
}

std::string señalCafe(double precio) {
    if (precio >= CAFE_TECHO_BONANZA)  return "BONANZA — Precio historico alto. Vende YA.";
    if (precio >= CAFE_ESTABLE_ALTO)   return "ALTO — Liquidez cafetera fuerte en la region.";
    if (precio >= CAFE_ESTABLE_BAJO)   return "NEUTRO — Mercado en equilibrio. Monitorea.";
    if (precio >= CAFE_PISO_RIESGO)    return "BAJO — Caficultores con presion. Precaucion.";
    return "CRITICO — Precios en minimos. Alto impacto local.";
}

// ============================================================
// MÓDULO 2 — SCORE TRM (peso: 30%)
// Lógica dual: TRM alta afecta importaciones pero ayuda exportadores
// Para Pitalito (exportador de café): TRM alta = bueno para el café
//                                      TRM alta = malo para insumos
// Neto: el efecto en costos domina → TRM alta = más riesgo general
// ============================================================

double calcularScoreTRM(double trm) {
    if (trm <= 0) return 50.0;

    if (trm <= TRM_BAJO)        return 20.0;  // Dólar barato: insumos baratos
    if (trm <= TRM_NEUTRAL_MAX) {
        double t = (trm - TRM_BAJO) / (TRM_NEUTRAL_MAX - TRM_BAJO);
        return 20.0 + (t * 20.0);  // 20% a 40%
    }
    if (trm <= TRM_ALTO) {
        double t = (trm - TRM_NEUTRAL_MAX) / (TRM_ALTO - TRM_NEUTRAL_MAX);
        return 40.0 + (t * 30.0);  // 40% a 70%
    }
    if (trm <= TRM_CRITICO) {
        double t = (trm - TRM_ALTO) / (TRM_CRITICO - TRM_ALTO);
        return 70.0 + (t * 20.0);  // 70% a 90%
    }
    return 95.0;
}

std::string señalTRM(double trm) {
    if (trm <= TRM_BAJO)        return "BAJO — Importaciones baratas. Buen momento tech.";
    if (trm <= TRM_NEUTRAL_MAX) return "NEUTRO — Dolar en rango saludable.";
    if (trm <= TRM_ALTO)        return "ALTO — Insumos importados mas caros. Ajusta precios.";
    if (trm <= TRM_CRITICO)     return "MUY ALTO — Presion de costos severa en la region.";
    return "CRITICO — Dolar en maximos historicos. Protegete.";
}

// ============================================================
// MÓDULO 3 — SCORE BANREP (peso: 20%)
// ============================================================

double calcularScoreBanRep(double tasa) {
    if (tasa <= 0) return 50.0;
    if (tasa <= BR_BAJO)        return 10.0;
    if (tasa <= BR_NEUTRAL) {
        double t = (tasa - BR_BAJO) / (BR_NEUTRAL - BR_BAJO);
        return 10.0 + (t * 25.0);
    }
    if (tasa <= BR_ALTO) {
        double t = (tasa - BR_NEUTRAL) / (BR_ALTO - BR_NEUTRAL);
        return 35.0 + (t * 35.0);
    }
    if (tasa <= BR_CRITICO) {
        double t = (tasa - BR_ALTO) / (BR_CRITICO - BR_ALTO);
        return 70.0 + (t * 25.0);
    }
    return 95.0;
}

std::string señalBanRep(double tasa) {
    if (tasa <= BR_BAJO)    return "BAJO — Credito accesible. Momento ideal para invertir.";
    if (tasa <= BR_NEUTRAL) return "MODERADO — Credito en zona aceptable.";
    if (tasa <= BR_ALTO)    return "ALTO — Credito costoso. Solo inversiones de alta rentabilidad.";
    return "CRITICO — Evita nuevas deudas a largo plazo.";
}

// ============================================================
// MÓDULO 4 — PROYECCIÓN (análisis de tendencia simple)
// Usa momentum del score actual para estimar 7 y 30 días
// ============================================================

double proyectarScore(double score, int dias) {
    // Sin historial real usamos la "inercia del mercado cafetero"
    // El mercado de café tiene ciclos de 45-90 días
    // Si está en bonanza (score bajo), la tendencia es a estabilizarse hacia 40-50
    // Si está en tormenta (score alto), tardará en recuperarse
    double objetivo = 45.0;  // Equilibrio histórico Pitalito
    double tasa_convergencia = 0.015 * dias;  // 1.5% por día hacia equilibrio
    
    double delta = (objetivo - score) * (1.0 - std::exp(-tasa_convergencia));
    double proyectado = score + delta;
    
    // Añadir ruido de mercado realista (±5%)
    double ruido = std::sin(score * 0.7 + dias) * 2.5;
    proyectado += ruido;
    
    return std::max(5.0, std::min(95.0, proyectado));
}

// ============================================================
// MÓDULO 5 — ESTIMADO DE LIQUIDEZ REGIONAL
// Basado en precio del café (el big driver económico de Pitalito)
// ============================================================

int estimarLiquidez(double cafe, double score) {
    double base = 0.0;
    if (cafe >= CAFE_TECHO_BONANZA)   base = 90.0;
    else if (cafe >= CAFE_ESTABLE_ALTO) base = 72.0;
    else if (cafe >= CAFE_ESTABLE_BAJO) base = 52.0;
    else if (cafe >= CAFE_PISO_RIESGO)  base = 32.0;
    else base = 18.0;

    // El score de riesgo modera el estimado de liquidez
    double ajuste = -(score - 50.0) * 0.2;
    return (int)std::max(10.0, std::min(95.0, base + ajuste));
}

// ============================================================
// RECOMENDACIÓN QUIRÚRGICA
// ============================================================

std::string generarRecomendacion(double score, double cafe, double trm, double br) {
    if (score < 25.0)
        return "ATAQUE: Bonanza maxima. Invierte en inventario, negocia con proveedores, expande.";
    if (score < 45.0)
        return "ACCION: Clima favorable. Gestiona creditos productivos y aumenta stock estrategico.";
    if (score < 65.0)
        return "EQUILIBRIO: Mantente firme. Cobra cartera, asegura 30 dias de caja, no te endeudes.";
    if (score < 80.0)
        return "DEFENSA: Riesgo elevado. Congela gastos, refuerza cobros, espera la proxima bonanza.";
    return "EMERGENCIA: Score critico. Modo supervivencia: liquidez primero, zero inversiones.";
}

// ============================================================
// SERIALIZACIÓN JSON (sin dependencias externas)
// ============================================================

std::string jsonString(const std::string& s) {
    // Escapa caracteres especiales para JSON válido
    std::string out = "\"";
    for (char c : s) {
        if (c == '"')       out += "\\\"";
        else if (c == '\\') out += "\\\\";
        else if (c == '\n') out += "\\n";
        else                out += c;
    }
    out += "\"";
    return out;
}

std::string toJSON(const ResultadoMotor& r, double cafe, double trm, double br) {
    std::ostringstream j;
    j << "{\n";
    j << "  \"score\":          " << (int)std::round(r.score)      << ",\n";
    j << "  \"clima\":          " << jsonString(r.clima)            << ",\n";
    j << "  \"score_cafe\":     " << (int)std::round(r.score_cafe) << ",\n";
    j << "  \"score_trm\":      " << (int)std::round(r.score_trm)  << ",\n";
    j << "  \"score_br\":       " << (int)std::round(r.score_br)   << ",\n";
    j << "  \"senal_cafe\":     " << jsonString(r.senal_cafe)       << ",\n";
    j << "  \"senal_trm\":      " << jsonString(r.senal_trm)        << ",\n";
    j << "  \"senal_br\":       " << jsonString(r.senal_br)         << ",\n";
    j << "  \"proyeccion_7d\":  " << (int)std::round(r.proj_7d)    << ",\n";
    j << "  \"proyeccion_30d\": " << (int)std::round(r.proj_30d)   << ",\n";
    j << "  \"liquidez_pct\":   " << r.liquidez_pct                << ",\n";
    j << "  \"recomendacion\":  " << jsonString(r.recomendacion)   << ",\n";
    j << "  \"inputs\": {\n";
    j << "    \"precio_cafe\": " << (long long)cafe   << ",\n";
    j << "    \"trm\":         " << trm                << ",\n";
    j << "    \"tasa_banrep\": " << br                 << "\n";
    j << "  }\n";
    j << "}";
    return j.str();
}

// ============================================================
// MAIN — Punto de entrada del Motor
// ============================================================

int main(int argc, char* argv[]) {
    // Leer argumentos de línea de comandos
    double cafe = 1800000.0;
    double trm  = 4200.0;
    double br   = 9.75;

    if (argc >= 2) cafe = std::atof(argv[1]);
    if (argc >= 3) trm  = std::atof(argv[2]);
    if (argc >= 4) br   = std::atof(argv[3]);

    // ===== CALCULAR COMPONENTES =====
    ResultadoMotor r;
    r.score_cafe = calcularScoreCafe(cafe);
    r.score_trm  = calcularScoreTRM(trm);
    r.score_br   = calcularScoreBanRep(br);

    // ===== SCORE PONDERADO FINAL =====
    r.score = (r.score_cafe * PESO_CAFE) +
              (r.score_trm  * PESO_TRM)  +
              (r.score_br   * PESO_BANREP);

    // Clamp estricto 0-100
    r.score = std::max(0.0, std::min(100.0, r.score));

    // ===== CLIMA =====
    if      (r.score <= 35.0) r.clima = "Bonanza";
    else if (r.score <= 65.0) r.clima = "Estabilidad";
    else                      r.clima = "Tormenta";

    // ===== SEÑALES =====
    r.senal_cafe = señalCafe(cafe);
    r.senal_trm  = señalTRM(trm);
    r.senal_br   = señalBanRep(br);

    // ===== PROYECCIONES =====
    r.proj_7d  = proyectarScore(r.score,  7);
    r.proj_30d = proyectarScore(r.score, 30);

    // ===== LIQUIDEZ REGIONAL =====
    r.liquidez_pct = estimarLiquidez(cafe, r.score);

    // ===== RECOMENDACIÓN =====
    r.recomendacion = generarRecomendacion(r.score, cafe, trm, br);

    // ===== OUTPUT JSON (para que scraper.py capture el resultado) =====
    std::cout << toJSON(r, cafe, trm, br) << std::endl;

    return 0;
}
