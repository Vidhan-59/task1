import Avatar from './Avatar';

const Card = ({ user, onClick }) => (
  <div className="cursor-pointer hover:shadow-lg transition-shadow border p-6 rounded-lg" onClick={onClick}>
    <Avatar src={user.image} alt={user.name} fallback={user.name.split(' ').map(n => n[0]).join('')} />
    <h2 className="text-xl font-semibold mb-2">{user.name}</h2>
    <p className="text-gray-600">{user.job_title}</p>
  </div>
);

export default Card;
