import React, { useState } from 'react';
import { auth } from './firebase';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword } from 'firebase/auth';

function AuthForm({ onAuth }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let userCred;
      if (isRegistering) {
        userCred = await createUserWithEmailAndPassword(auth, email, password);
        setMessage("✅ Usuario registrado");
      } else {
        userCred = await signInWithEmailAndPassword(auth, email, password);
        setMessage("✅ Usuario autenticado");
      }

      if (onAuth) onAuth(userCred.user);  // Asegura que esté definido
    } catch (error) {
      setMessage("❌ " + error.message);
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: '400px' }}>
      <h3 className="mb-4">{isRegistering ? 'Registrarse' : 'Iniciar sesión'}</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group mb-3">
          <label>Correo electrónico</label>
          <input
            type="email"
            className="form-control"
            placeholder="usuario@correo.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group mb-4">
          <label>Contraseña</label>
          <input
            type="password"
            className="form-control"
            placeholder="********"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn btn-primary w-100">
          {isRegistering ? 'Registrarse' : 'Entrar'}
        </button>
      </form>
      <div className="form-text mt-3 text-center">
        {isRegistering ? '¿Ya tienes cuenta?' : '¿No tienes cuenta?'}{' '}
        <button className="btn btn-link p-0" onClick={() => setIsRegistering(!isRegistering)}>
          {isRegistering ? 'Inicia sesión' : 'Regístrate'}
        </button>
      </div>
      {message && <div className="alert alert-info mt-3">{message}</div>}
    </div>
  );
}

export default AuthForm;
