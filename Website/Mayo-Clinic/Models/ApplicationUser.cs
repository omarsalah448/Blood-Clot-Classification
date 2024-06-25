using Microsoft.AspNetCore.Identity;

namespace Mayo_Clinic.Models
{
    public class ApplicationUser : IdentityUser
    {
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public DateOnly BirthDate { get; set; }

    }
}
