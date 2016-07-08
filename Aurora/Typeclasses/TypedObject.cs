using System;

using ServiceStack.DataAnnotations;

namespace Aurora.Typeclasses
{
    public abstract class TypedObject
    {
        [Required]
        [StringLength(255)]
        [Index(Unique = true)]
        public string Key { get; set; }
        public string Name { get; set; }
        public string TypeclassPath { get; set; }
        public TypedObject Typeclass { get; set; }
        public DateTime DateCreated { get; set; }
        public string Permissions { get; set; }
        public string Dbref { get; set; }
        public string ObjID { get; set; }
        public string Attributes { get; set; }
    }
}
