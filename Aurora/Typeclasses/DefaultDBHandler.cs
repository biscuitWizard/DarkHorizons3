using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Text;
using System.Threading.Tasks;

using Aurora.Typeclasses.Factories;

namespace Aurora.Typeclasses
{
    public class DefaultDBHandler : IDBHandler
    {
        public ObjectBase[] ObjectsBase { get; protected set; }

        public Exit[] Exits { get; protected set; }

        public Character[] Characters { get; protected set; }

        public Player[] Players { get; protected set; }

        public Room[] Rooms { get; protected set; }

        public IList<IObjectFactory<ObjectBase>> Factories { get; protected set; }

        private readonly IDictionary<long, ObjectBase> objects 
            = new Dictionary<long, ObjectBase>();
        /// <summary>
        /// Initializes a new instance of the <see cref="DefaultDBHandler"/> class.
        /// </summary>
        public DefaultDBHandler()
        {
            
        }

        public virtual void AddObject(ObjectBase o)
        {
            if (!o.DbID.HasValue)
            {
                // Save to DB.
            }

            // Add to handler.
            objects.Add(o.DbID.Value, o);
        }

        public virtual TObject CreateObject<TObject>(long? dbID = null) where TObject : ObjectBase
        {
            IObjectFactory<ObjectBase> factory = Factories.FirstOrDefault(f => f is IObjectFactory<TObject>);
            if (factory == null)
            {
                // Unable to find a suitable factory. Make a default object instead.
                factory = new DefaultObjectFactory();
            }

            TObject instance = factory.CreateInstance();
            AddObject(instance);
            return instance;
        }

        public virtual void DestroyObject<TObject>(Expression<Func<TObject, bool>> deleteExpression)
        {
            throw new NotImplementedException();
        }

        public virtual void DestroyObject(long dbID)
        {
            throw new NotImplementedException();
        }

        public virtual TObject[] FindObjects<TObject>(Expression<Func<TObject, bool>> whereExpression)
        {
            throw new NotImplementedException();
        }

        public virtual void SaveChanges()
        {
            throw new NotImplementedException();
        }
    }
}
