using System;
using System.Linq.Expressions;

using Aurora.Typeclasses.Factories;

namespace Aurora.Typeclasses
{
    public interface IDBHandler
    {
        ObjectBase[] ObjectsBase { get; }
        Exit[] Exits { get;  }
        Character[] Characters { get; }
        Player[] Players { get; }
        Room[] Rooms { get; }
        IObjectFactory<ObjectBase> Factories { get; }

        void AddObject(ObjectBase o);

        TObject CreateObject<TObject>(long? dbID = null) where TObject : ObjectBase;

        void DestroyObject<TObject>(Expression<Func<TObject, bool>> deleteExpression);

        void DestroyObject(long dbID);

        TObject[] FindObjects<TObject>(Expression<Func<TObject, bool>> whereExpression);

        void SaveChanges();
    }
}
