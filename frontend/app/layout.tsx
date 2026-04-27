import type { Metadata } from 'next';
import AppShell from '@/components/AppShell';

export const metadata: Metadata = {
  title: 'IRWT - Pedidos de Vans',
  description: 'Gestao de pedidos de aluguer de vans',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body style={{
        margin: 0,
        fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
        backgroundColor: '#f8fafc',
        minHeight: '100vh',
      }}>
        <AppShell>
          {children}
        </AppShell>
      </body>
    </html>
  );
}
