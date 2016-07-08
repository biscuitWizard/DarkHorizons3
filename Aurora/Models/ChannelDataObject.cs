using Aurora.Typeclasses;

using ServiceStack.DataAnnotations;

namespace Aurora.Models
{
    public class ChannelDataObject : TypedObject
    {
        [AutoIncrement]
        public long ID { get; set; }
    }
}
