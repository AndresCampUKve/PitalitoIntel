import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  Newspaper, 
  ShieldAlert, 
  Lightbulb, 
  Menu, 
  Clock, 
  Globe, 
  Cpu, 
  Zap,
  Coffee,
  DollarSign,
  Percent,
  History,
  Activity,
  Box,
  Smartphone
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';
import { supabase } from './supabase';
import './App.css';

const App = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  useEffect(() => {
    fetchData();
    const subscription = supabase
      .channel('clima_updates')
      .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'clima_historico' }, fetchData)
      .subscribe();

    return () => {
      supabase.removeChannel(subscription);
    };
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      // Latest data
      const { data: climaData } = await supabase
        .from('clima_historico')
        .select('*')
        .order('fecha', { ascending: false })
        .limit(1);

      if (climaData?.length > 0) setData(climaData[0]);

      // Historical data (last 10 days)
      const { data: histData } = await supabase
        .from('clima_historico')
        .select('fecha, score_riesgo, precio_cafe, trm')
        .order('fecha', { ascending: true })
        .limit(15);

      if (histData) setHistory(histData.map(h => ({
        ...h,
        fecha: h.fecha.split('-').slice(1).join('/') // Format MM/DD
      })));

      // News
      const { data: newsData } = await supabase
        .from('noticias')
        .select('*')
        .order('fecha', { ascending: false })
        .limit(6);

      if (newsData) setNews(newsData);
      
      setLastUpdate(new Date());
    } catch (err) {
      console.error("Error fetching data:", err);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score < 35) return 'var(--success)';
    if (score < 65) return 'var(--warn)';
    return 'var(--danger)';
  };

  return (
    <div className="app-container">
      <aside className="sb">
        <div className="sb-logo-name">✹ Bonanza</div>
        
        <div className="sb-section">ANÁLISIS</div>
        <button className={`sb-item ${activeTab === 'overview' ? 'active' : ''}`} onClick={() => setActiveTab('overview')}>
          <TrendingUp size={18} /> Overview
        </button>
        <button className={`sb-item ${activeTab === 'history' ? 'active' : ''}`} onClick={() => setActiveTab('history')}>
          <History size={18} /> Historial
        </button>
        <button className={`sb-item ${activeTab === 'news' ? 'active' : ''}`} onClick={() => setActiveTab('news')}>
          <Newspaper size={18} /> Noticias
        </button>

        <div className="sb-section">PREDICCIONES (IA)</div>
        <button className="sb-item opacity-50 cursor-not-allowed"><Cpu size={18} /> Futuro Café</button>

        <div className="sb-section">ECOSISTEMA</div>
        <div className="sb-item"><Box size={18} /> Docker Cloud</div>
        <div className="sb-item"><Smartphone size={18} /> Pitalito Mobile</div>
        
        <div className="mt-auto pt-4 border-t border-white/5 opacity-50 text-[10px] font-mono">
          ESTADO: OPERATIVO | PITALITO v2.5
        </div>
      </aside>

      <main className="main">
        <header className="ph">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="pt">Dashboard Inteligente</h1>
              <p className="text-xs font-mono text-muted mt-1 uppercase tracking-widest">
                Real-Time FNC Feed | Sync: {lastUpdate.toLocaleTimeString()}
              </p>
            </div>
            {data && (
              <span className={`px-3 py-1 rounded-full text-xs font-bold border ${data.clima === 'Bonanza' ? 'bg-success/10 text-success border-success' : data.clima === 'Tormenta' ? 'bg-danger/10 text-danger border-danger' : 'bg-warn/10 text-warn border-warn'}`}>
                {data.clima}
              </span>
            )}
          </div>
        </header>

        <AnimatePresence mode="wait">
          {activeTab === 'overview' && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}>
              <div className="score-card">
                <div className="flex justify-between items-end mb-4">
                  <div>
                    <p className="text-[10px] font-bold text-muted uppercase">Nivel de Riesgo Regional</p>
                    <h2 className="score-num" style={{ color: getScoreColor(data?.score_riesgo) }}>{data?.score_riesgo || '--'}%</h2>
                  </div>
                  <div className="text-right">
                    <p className="text-[10px] font-bold text-muted uppercase">IA Trend</p>
                    <p className="text-sm font-bold flex items-center gap-1"><Zap size={14} className="text-purple-400" /> Bajando</p>
                  </div>
                </div>
                <div className="score-bar-bg"><div className="score-bar-fill" style={{ width: `${data?.score_riesgo || 0}%`, backgroundColor: getScoreColor(data?.score_riesgo) }} /></div>
                <div className="flex justify-between text-[9px] font-mono text-muted uppercase"><span>Bonanza</span><span>Estabilidad</span><span>Tormenta</span></div>
              </div>

              <div className="mg">
                <div className="mc"><p className="mc-l">Café (FNC)</p><div className="mc-v text-success">${data?.precio_cafe?.toLocaleString()}</div></div>
                <div className="mc"><p className="mc-l">TRM Hoy</p><div className="mc-v text-accent">${data?.trm?.toLocaleString()}</div></div>
                <div className="mc"><p className="mc-l">BanRep</p><div className="mc-v text-warn">{data?.tasa_banrep}%</div></div>
              </div>
            </motion.div>
          )}

          {activeTab === 'history' && (
            <motion.div initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }} className="space-y-6">
              <div className="mc h-[300px]">
                <p className="mc-l mb-4 flex items-center gap-2"><Activity size={12} /> Histórico de Riesgo (Momentum)</p>
                <ResponsiveContainer width="100%" height="80%">
                  <AreaChart data={history}>
                    <defs>
                      <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <XAxis dataKey="fecha" stroke="#8b92a5" fontSize={10} axisLine={false} tickLine={false} />
                    <Tooltip contentStyle={{ backgroundColor: '#151821', border: 'none', borderRadius: '8px', fontSize: '10px' }} />
                    <Area type="monotone" dataKey="score_riesgo" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorRisk)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="mc h-[200px]">
                  <p className="mc-l mb-4">Precio Café (COP)</p>
                  <ResponsiveContainer width="100%" height="70%">
                    <LineChart data={history}>
                      <Line type="monotone" dataKey="precio_cafe" stroke="#00d084" dot={false} strokeWidth={2} />
                      <XAxis dataKey="fecha" hide />
                      <Tooltip contentStyle={{ background: '#151821' }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
                <div className="mc h-[200px]">
                  <p className="mc-l mb-4">Dólar (TRM)</p>
                  <ResponsiveContainer width="100%" height="70%">
                    <LineChart data={history}>
                      <Line type="monotone" dataKey="trm" stroke="#ffffff" dot={false} strokeWidth={2} />
                      <XAxis dataKey="fecha" hide />
                      <Tooltip contentStyle={{ background: '#151821' }} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'news' && (
            <div className="grid grid-cols-2 gap-4">
              {news.map(n => (
                <div key={n.id} className="news-card hover:translate-x-1 border-l-2 border-accent transition-all cursor-pointer">
                  <h3 className="text-sm font-bold mb-2">{n.titulo}</h3>
                  <div className="flex justify-between text-[10px] opacity-40"><span>{n.fuente}</span><span>{new Date(n.fecha).toLocaleDateString()}</span></div>
                </div>
              ))}
            </div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
};

export default App;
