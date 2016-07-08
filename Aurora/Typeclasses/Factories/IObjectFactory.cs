namespace Aurora.Typeclasses.Factories
{
    public interface IObjectFactory<out TObject> where TObject : ObjectBase
    {
        TObject CreateInstance();
    }
}
