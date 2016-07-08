using Aurora.Typeclasses;

using ServiceStack.DataAnnotations;

namespace Aurora.Models
{
    public class ObjectDataObject : TypedObject
    {
        [AutoIncrement]
        public long ID { get; set; }
    }
}
