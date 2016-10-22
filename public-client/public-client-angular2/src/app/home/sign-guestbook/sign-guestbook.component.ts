import { Component } from '@angular/core';
import { GuestbookEntry }    from '../../shared/api.model';
import { ApiService } from '../../shared/api.service';
import { Router } from '@angular/router';

@Component({
    selector: 'sign-guestbook',
    templateUrl: 'sign-guestbook.component.html',
    styleUrls: ['./sign-guestbook.component.scss']
})
export class SignGuestbookComponent {
    model: GuestbookEntry = null;
    state_submitted: boolean = false;
    state_completed: boolean = false;

    constructor(private api: ApiService, private router: Router) {
        this.resetState();
        this.resetModel();
    }

    onSubmit() {
        this.state_submitted = true;
        this.observeGuestbookPost(this.model);
    }

    observeGuestbookPost(entry: GuestbookEntry): void {
        this.api.signGuestbook(entry)
            .subscribe(
                new_entry => this.handlePostComplete(new_entry),
                error => console.error('Error: ' + error)
            )
    }

    signAgainButtonClick(): void {
        this.resetModel();
        this.resetState();
    }

    browseButtonClick(): void {
        this.router.navigate(['/browse']);
    }

    private handlePostComplete(new_entry: GuestbookEntry): void {
        this.model = new_entry;
        this.state_completed = true;
        console.log('New guestbook entry: '+JSON.stringify(new_entry));
    }

    resetState(): void {
        this.state_submitted = false;
        this.state_completed = false;
    }

    resetModel(): void {
        this.model = new GuestbookEntry(null, null, null, null);
    }

    // TODO: Remove this when we're done
    get diagnostic() { return JSON.stringify(this.model) + ' && state_submitted: ' + this.state_submitted + ' && state_completed: ' + this.state_completed; }
}