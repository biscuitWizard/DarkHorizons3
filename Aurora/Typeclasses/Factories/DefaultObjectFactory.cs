using System;

namespace Aurora.Typeclasses.Factories
{
    public class DefaultObjectFactory : IObjectFactory<DefaultObject>
    {
        public DefaultObject CreateInstance()
        {
            throw new NotImplementedException();
        }
    }
}
