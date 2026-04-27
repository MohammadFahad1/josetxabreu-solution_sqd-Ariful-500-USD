'use client';

import { Toaster } from 'sonner';
import AuthGuard from './AuthGuard';

interface AppShellProps {
  children: React.ReactNode;
}

export default function AppShell({ children }: AppShellProps) {
  return (
    <AuthGuard>
      <nav style={{
        backgroundColor: '#ffffff',
        borderBottom: '1px solid #e2e8f0',
        padding: '12px 32px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        position: 'sticky',
        top: 0,
        zIndex: 100,
        boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <img
            src="https://res.cloudinary.com/dsntusqam/image/upload/v1765271950/logo_eaj0du.png"
            alt="IRWT Logo"
            style={{ height: '40px', width: 'auto' }}
          />
          <div style={{ height: '24px', width: '1px', backgroundColor: '#e2e8f0' }} />
          <span style={{
            fontSize: '14px',
            fontWeight: 500,
            color: '#64748b',
            letterSpacing: '-0.01em',
          }}>
            Gestao de Pedidos
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <a href="/" style={{
            color: '#1e293b',
            textDecoration: 'none',
            fontSize: '14px',
            fontWeight: 500,
            padding: '8px 16px',
            borderRadius: '8px',
            backgroundColor: '#f1f5f9',
            transition: 'all 0.2s',
          }}>
            Painel
          </a>
          <a href="/metrics" style={{
            color: '#1e293b',
            textDecoration: 'none',
            fontSize: '14px',
            fontWeight: 500,
            padding: '8px 16px',
            borderRadius: '8px',
            backgroundColor: '#f1f5f9',
            transition: 'all 0.2s',
          }}>
            Metricas
          </a>
        </div>
      </nav>
      <main style={{ maxWidth: '1280px', margin: '0 auto', padding: '32px' }}>
        {children}
      </main>
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
          },
        }}
        richColors
        closeButton
      />
    </AuthGuard>
  );
}
