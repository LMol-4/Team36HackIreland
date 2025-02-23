import { FaGithub } from 'react-icons/fa';

const Navbar = () => {
  return (
    <nav className="fixed top-0 left-0 right-0 p-6 backdrop-blur-sm bg-white/50 z-50 border-b border-emerald-100/20">
      <div className="max-w-6xl mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <a href="/" className="flex items-center space-x-2">
            <img src="/circle-logo.png" alt="Circle Logo" className="h-8 w-8" />
            <span className="text-xl font-semibold text-gray-800">Pitch Perfect</span>
          </a>
        </div>
        <div className="flex space-x-8">
          <a href="https://github.com/LMol-4/Team36HackIreland"  target="_blank" className="text-gray-600 hover:text-emerald-600 transition-colors flex items-center space-x-2 p-2">
            <FaGithub className="text-gray-600 transition-colors" size={20} />
            <span>Github</span>
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;