<template>
  <div>
    <v-dialog
      v-model="dialog"
      max-width="250px">
      <v-card>
        <v-card-title>
          <span class="headline">{{ formTitle }}</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout
              column>
              <v-flex
                xs12
                sm6
                md4>
                <v-text-field
                  v-model.number="showtimeTicket['seat']"
                  label="Seat"
                  type="number"/>
              </v-flex>
              <v-flex
                xs12
                sm6
                md4>
                <v-text-field
                  v-model="showtimeTicket['discount']"
                  label="Discount"
                  type="number"/>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn
            color="blue darken-1"
            flat
            @click="dialog = false">Cancel</v-btn>
          <v-btn
            color="blue darken-1"
            flat
            @click="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-layout row>
      <v-flex
        s12
        sm5
        md5
        offset-lg
      >
        Repertoire:
        <v-data-table
          :headers="showtimeHeaders"
          :items="repertoire"
          class="elevation-1"
        >
          <template
            slot="items"
            slot-scope="props">
            <td> {{ getMovie(props.item.movie).title }}</td>
            <td> {{ props.item.auditorium }}</td>
            <td> {{ props.item.date }}</td>
            <td> {{ props.item.time }}</td>
            <td> {{ props.item.price }}</td>
            <v-tooltip right>
              <v-btn
                slot="activator"
                icon
                @click="create(props.item)">
                <v-icon>add</v-icon>
              </v-btn>
              <span>new ticket</span>
            </v-tooltip>
          </template>
          <template slot="no-data">
            Nothing to show
          </template>
        </v-data-table>
      </v-flex>
      <v-flex
        s12
        sm5
        md6
        offset-lg1
      >
        Tickets on sale:
        <v-data-table
          :items="tickets"
          :headers="ticketsHeaders"
          item-key="date"
          class="elevation-1"
        >
          <template
            slot="items"
            slot-scope="props">
            <td>{{ getMovie(getShowtime(props.item.showtime).movie).title }}</td>
            <td>{{ getShowtime(props.item.showtime).auditorium }} </td>
            <td>{{ props.item.seat }} </td>
            <td>{{ getShowtime(props.item.showtime).date }}</td>
            <td>{{ getShowtime(props.item.showtime).time }}</td>
            <td>{{ getShowtime(props.item.showtime).price }}</td>
            <td>{{ props.item.discount }}</td>
            <td class="justify-center layout px-0">
              <v-btn
                slot="activator"
                icon
                @click="editButton(props.item)">
                <v-icon>edit</v-icon>
              </v-btn>
              <v-btn
                slot="activator"
                icon
                @click="deleteButton(props.item.id)">
                <v-icon>delete</v-icon>
              </v-btn>
            </td>
            <v-dialog
              v-model="confirmDelete"
              persistent
              max-width="300px"
            >
              <v-card>
                <v-card-text>
                  Delete this ticket?
                </v-card-text>
                <v-card-actions>
                  <v-btn @click="remove">yes</v-btn>
                  <v-spacer/>
                  <v-btn @click="confirmDelete = false">no</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </template>
          <template slot="no-data">
            Sorry, nothing to display here.
          </template>
        </v-data-table>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
import SysAdminController from 'Controllers/system-admin.controller';
import TheaterController from 'Controllers/theaters.controller';
import TicketOnSaleController from 'Controllers/tickets-on-sale.controller';
import { Movie } from 'Models/movie.model';
import { TicketOnSale } from 'Models/ticket-on-sale.model';
import { mapGetters } from 'vuex';

export default {
  data: () => ({
    movies: [],
    movie: new Movie(),
    confirmDelete: false,
    ticketToDelete: 0,
    theaterId: 0,
    dialog: false,
    showtimeTicket: new TicketOnSale(),
    repertoire: [],
    discount: 0,
    seat: 0,
    tickets: [],
    editedIndex: -1
  }),
  computed: {
    ...mapGetters([
      'activeUser',
      'headers',
      'showtimeHeaders',
      'ticketsHeaders'
    ]),
    formTitle() {
      return this.editedIndex === -1 ? 'New ticket' : 'Edit ticket';
    }
  },
  mounted() {
    this.getTheater();
  },
  methods: {
    create(showtime) {
      this.dialog = true;
      this.showtimeTicket = new TicketOnSale(showtime);
      this.editedIndex = -1;
    },
    save() {
      this.dialog = false;
      if (this.editedIndex === -1) {
        this.showtimeTicket['theater'] = this.theaterId;
        this.showtimeTicket['showtime'] = this.showtimeTicket['id'];
        TicketOnSaleController.create(this.showtimeTicket)
          .then((response) => {
            this.$alert.success('Successfully added!');
            this.getTickets();
          })
          .catch((response) => {
            this.$alert.error('Error occurred.');
          });
      } else {
        let data = _.reduce(this.showtimeTicket, (result, value, key) => {
          if (!_.isEmpty(value)) {
            result[key] = value;
          }
          return result;
        }, {});
        TicketOnSaleController.update(data, this.showtimeTicket.id).then((response) => {
          this.dialog = false;
          this.showtimeTicket = new TicketOnSale(response.data);
          this.$alert.success('Settings successfully saved');
        }).catch(() => {
          this.$alert.error('Error while saving settings');
        });
      }
    },
    getTheater() {
      SysAdminController.getTheater(this.activeUser.id)
        .then((response) => {
          this.theaterId = response.data.id;
          this.getMovies();
          this.getRepertoire();
          this.getTickets();
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    getMovies(id = this.theaterId) {
      SysAdminController.getMovies(id)
        .then((response) => {
          this.movies = _.map(response.data, x => new Movie(x));
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    getRepertoire(id = this.theaterId) {
      TheaterController.getRepertoire(id)
        .then((response) => {
          this.repertoire = _.map(response.data, x => new TicketOnSale(x));
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    getTickets(id = this.theaterId) {
      TheaterController.getTicketsOnSale(id)
        .then((response) => {
          this.tickets = _.map(response.data, x => new TicketOnSale(x));
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    deleteButton(id) {
      this.confirmDelete = true;
      this.ticketToDelete = id;
    },
    remove() {
      this.confirmDelete = false;
      TicketOnSaleController.destroy(this.ticketToDelete)
        .then((response) => {
          this.$alert.success('Successfully deleted!');
          this.getTickets();
        })
        .catch((response) => {
          this.$alert.error('Error occurred.');
        });
    },
    editButton(ticketData) {
      this.showtimeTicket = ticketData;
      this.editedIndex = 1;
      this.dialog = true;
    },
    getMovie(id) {
      return this.movies.find((element) => {
        return element.id === id;
      });
    },
    getShowtime(id) {
      return this.repertoire.find((element) => {
        return element.id === id;
      });
    }
  }
};
</script>
