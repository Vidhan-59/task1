const Avatar = ({ src, alt, fallback }) => (
    <div className="w-24 h-24 mb-4 bg-gray-200 rounded-full flex items-center justify-center">
      {src ? <img src={src} alt={alt} className="w-full h-full rounded-full" /> : <span>{fallback}</span>}
    </div>
  )
  
  export default Avatar;
  