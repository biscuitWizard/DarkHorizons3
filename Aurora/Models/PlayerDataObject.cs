using Aurora.Typeclasses;

using ServiceStack.DataAnnotations;

namespace Aurora.Models
{
    public class PlayerDataObject : TypedObject
    {
        [AutoIncrement]
        public long ID { get; set; }

        public bool IsBit { get; set; }
        public bool IsConnected { get; set; }
        public bool IsSuperUser { get; set; }
        public int[] Sessions { get; set; }

    }
}
