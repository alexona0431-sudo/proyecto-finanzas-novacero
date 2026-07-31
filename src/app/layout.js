import "./globals.css";

export const metadata = {
  title: "Novacero | Evaluación financiera y fotovoltaica",
  description:
    "Dashboard académico de análisis económico, financiero e ingeniería económica de Novacero S.A.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
