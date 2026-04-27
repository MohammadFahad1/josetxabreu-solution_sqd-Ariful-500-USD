'use client';

import { useState, useEffect } from 'react';

interface AuthGuardProps {
  children: React.ReactNode;
}

export default function AuthGuard({ children }: AuthGuardProps) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if already authenticated
    const auth = sessionStorage.getItem('irwt_auth');
    if (auth === 'true') {
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const res = await fetch('/api/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password }),
      });

      if (res.ok) {
        sessionStorage.setItem('irwt_auth', 'true');
        setIsAuthenticated(true);
      } else {
        setError('Palavra-passe incorreta');
      }
    } catch {
      setError('Erro ao autenticar');
    }
  };

  if (loading) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f8fafc',
      }}>
        <p style={{ color: '#64748b' }}>A carregar...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f8fafc',
        fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
      }}>
        <div style={{
          backgroundColor: '#ffffff',
          padding: '40px',
          borderRadius: '16px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.05), 0 10px 20px rgba(0, 0, 0, 0.1)',
          width: '100%',
          maxWidth: '400px',
          margin: '20px',
        }}>
          <div style={{ textAlign: 'center', marginBottom: '32px' }}>
            <img
              src="https://res.cloudinary.com/dsntusqam/image/upload/v1765271950/logo_eaj0du.png"
              alt="IRWT Logo"
              style={{ height: '50px', width: 'auto', marginBottom: '16px' }}
            />
            <h1 style={{
              margin: '0 0 8px',
              fontSize: '24px',
              fontWeight: 700,
              color: '#0f172a',
            }}>
              Painel de Gestao
            </h1>
            <p style={{
              margin: 0,
              fontSize: '14px',
              color: '#64748b',
            }}>
              Introduza a palavra-passe para aceder
            </p>
          </div>

          <form onSubmit={handleLogin}>
            <div style={{ marginBottom: '20px' }}>
              <label style={{
                display: 'block',
                marginBottom: '8px',
                fontSize: '14px',
                fontWeight: 500,
                color: '#475569',
              }}>
                Palavra-passe
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Introduza a palavra-passe"
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  borderRadius: '8px',
                  border: '1px solid #e2e8f0',
                  fontSize: '14px',
                  outline: 'none',
                  boxSizing: 'border-box',
                }}
              />
            </div>

            {error && (
              <div style={{
                backgroundColor: '#fef2f2',
                color: '#dc2626',
                padding: '12px 16px',
                borderRadius: '8px',
                marginBottom: '20px',
                fontSize: '14px',
                border: '1px solid #fecaca',
              }}>
                {error}
              </div>
            )}

            <button
              type="submit"
              style={{
                width: '100%',
                padding: '12px 24px',
                borderRadius: '8px',
                border: 'none',
                backgroundColor: '#0f172a',
                color: '#ffffff',
                fontSize: '14px',
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.2s',
              }}
            >
              Entrar
            </button>
          </form>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
